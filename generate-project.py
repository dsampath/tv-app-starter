"""Generate a dependency-free Xcode project from the app sources."""
from pathlib import Path
import hashlib
import json
import re

root = Path(__file__).resolve().parent
def uid(name): return hashlib.sha1(name.encode()).hexdigest()[:24].upper()
def q(value): return json.dumps(str(value))
(root / 'FamilyTV.xcodeproj/xcshareddata/xcschemes').mkdir(parents=True, exist_ok=True)
objects = []
def obj(name, body):
    key = uid(name)
    objects.append(f'{key} = {{ {body} }};')
    return key
source_refs, builds = [], []
for path in sorted((root / 'FamilyTV').glob('*.swift')) + sorted((root / 'Core').glob('*.swift')):
    rel = str(path.relative_to(root))
    ref = obj(rel, f'isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = {q(rel)}; sourceTree = "<group>";')
    source_refs.append(ref)
    builds.append(obj(rel + '-build', f'isa = PBXBuildFile; fileRef = {ref};'))
product = obj('product', 'isa = PBXFileReference; explicitFileType = wrapper.application; path = FamilyTV.app; sourceTree = BUILT_PRODUCTS_DIR;')
products = obj('products', f'isa = PBXGroup; children = ({product}); name = Products; sourceTree = "<group>";')
group = obj('group', f'isa = PBXGroup; children = ({",".join(source_refs + [products])}); sourceTree = "<group>";')
sources = obj('sources', f'isa = PBXSourcesBuildPhase; buildActionMask = 2147483647; files = ({",".join(builds)}); runOnlyForDeploymentPostprocessing = 0;')
resources = obj('resources', f'isa = PBXResourcesBuildPhase; buildActionMask = 2147483647; files = (); runOnlyForDeploymentPostprocessing = 0;')
frameworks = obj('frameworks', 'isa = PBXFrameworksBuildPhase; buildActionMask = 2147483647; files = (); runOnlyForDeploymentPostprocessing = 0;')
base = {'SDKROOT':'appletvos', 'TVOS_DEPLOYMENT_TARGET':'17.0', 'SWIFT_VERSION':'5.0', 'CLANG_ENABLE_MODULES':'YES', 'TARGETED_DEVICE_FAMILY':'3', 'SUPPORTED_PLATFORMS':'appletvos appletvsimulator', 'PRODUCT_BUNDLE_IDENTIFIER':'org.example.tvstarter', 'PRODUCT_NAME':'$(TARGET_NAME)', 'GENERATE_INFOPLIST_FILE':'YES', 'INFOPLIST_KEY_CFBundleDisplayName':'TV Starter', 'INFOPLIST_KEY_UILaunchScreen_Generation':'YES', 'MARKETING_VERSION':'0.1.0', 'CURRENT_PROJECT_VERSION':'1', 'CODE_SIGN_STYLE':'Automatic', 'ENABLE_USER_SCRIPT_SANDBOXING':'YES', 'SWIFT_EMIT_LOC_STRINGS':'YES'}
base['INFOPLIST_FILE'] = 'FamilyTV/Info.plist'

def config(name, settings): return obj(name, 'isa = XCBuildConfiguration; buildSettings = {' + ''.join(f'{k} = {q(v)};' for k,v in settings.items()) + '}; name = ' + ('Debug' if name.endswith('Debug') else 'Release') + ';')
configs = [config('target-Debug', {**base, 'SWIFT_OPTIMIZATION_LEVEL':'-Onone', 'SWIFT_ACTIVE_COMPILATION_CONDITIONS':'DEBUG'}), config('target-Release',{**base, 'SWIFT_OPTIMIZATION_LEVEL':'-O'})]
target_config = obj('target-config', f'isa = XCConfigurationList; buildConfigurations = ({",".join(configs)}); defaultConfigurationIsVisible = 0; defaultConfigurationName = Release;')
project_configs = [config('project-Debug', {}), config('project-Release', {})]
project_config = obj('project-config', f'isa = XCConfigurationList; buildConfigurations = ({",".join(project_configs)}); defaultConfigurationIsVisible = 0; defaultConfigurationName = Release;')
target = obj('target', f'isa = PBXNativeTarget; buildConfigurationList = {target_config}; buildPhases = ({sources},{frameworks},{resources}); buildRules = (); dependencies = (); name = FamilyTV; productName = FamilyTV; productReference = {product}; productType = "com.apple.product-type.application";')
project = obj('project', f'isa = PBXProject; attributes = {{LastUpgradeCheck = 2700;}}; buildConfigurationList = {project_config}; compatibilityVersion = "Xcode 14.0"; developmentRegion = en; hasScannedForEncodings = 0; knownRegions = (en,Base); mainGroup = {group}; productRefGroup = {products}; projectDirPath = ""; projectRoot = ""; targets = ({target});')
(root / 'FamilyTV.xcodeproj/project.pbxproj').write_text('// !$*UTF8*$!\n{archiveVersion = 1; classes = {}; objectVersion = 56; objects = {\n' + '\n'.join(objects) + f'\n}}; rootObject = {project};}}\n')
scheme = f'''<?xml version="1.0" encoding="UTF-8"?>
<Scheme LastUpgradeVersion="2700" version="1.3"><BuildAction parallelizeBuildables="YES" buildImplicitDependencies="YES"><BuildActionEntries><BuildActionEntry buildForTesting="YES" buildForRunning="YES" buildForProfiling="YES" buildForArchiving="YES" buildForAnalyzing="YES"><BuildableReference BuildableIdentifier="primary" BlueprintIdentifier="{target}" BuildableName="FamilyTV.app" BlueprintName="FamilyTV" ReferencedContainer="container:FamilyTV.xcodeproj"/></BuildActionEntry></BuildActionEntries></BuildAction><LaunchAction buildConfiguration="Debug" selectedDebuggerIdentifier="Xcode.DebuggerFoundation.Debugger.LLDB" selectedLauncherIdentifier="Xcode.IDEFoundation.Launcher.LLDB" launchStyle="0" useCustomWorkingDirectory="NO" ignoresPersistentStateOnLaunch="NO" debugDocumentVersioning="YES" allowLocationSimulation="YES"><BuildableProductRunnable runnableDebuggingMode="0"><BuildableReference BuildableIdentifier="primary" BlueprintIdentifier="{target}" BuildableName="FamilyTV.app" BlueprintName="FamilyTV" ReferencedContainer="container:FamilyTV.xcodeproj"/></BuildableProductRunnable></LaunchAction><ProfileAction buildConfiguration="Release" shouldUseLaunchSchemeArgsEnv="YES"/><AnalyzeAction buildConfiguration="Debug"/><ArchiveAction buildConfiguration="Release" revealArchiveInOrganizer="YES"/></Scheme>'''
(root / 'FamilyTV.xcodeproj/xcshareddata/xcschemes/FamilyTV.xcscheme').write_text(scheme)
print('Generated FamilyTV.xcodeproj')
