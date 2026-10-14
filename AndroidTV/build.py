"""Build the local Google TV APK using the Android SDK, without Gradle dependencies."""
from pathlib import Path
import os,subprocess,zipfile,shutil
root=Path(__file__).resolve().parent
sdk_value=os.environ.get('ANDROID_SDK_ROOT') or os.environ.get('ANDROID_HOME')
if not sdk_value: raise SystemExit('Set ANDROID_SDK_ROOT to your Android SDK directory.')
sdk=Path(sdk_value)
java_home=os.environ.get('JAVA_HOME')
if not java_home: raise SystemExit('Set JAVA_HOME to your JDK 17 directory.')
jdk=Path(java_home)
env=dict(os.environ,JAVA_HOME=str(jdk));env['PATH']=str(jdk/'bin')+':'+env['PATH']
tools=sdk/'build-tools'/os.environ.get('ANDROID_BUILD_TOOLS','35.0.0');android=sdk/'platforms/android-35/android.jar';build=root/'build';build.mkdir(exist_ok=True)
def run(*args):subprocess.run([str(x) for x in args],check=True,env=env,cwd=root)
run(tools/'aapt2','compile','--dir',root/'res','-o',build/'resources.zip')
run(tools/'aapt2','link','-o',build/'unsigned.apk','--manifest',root/'AndroidManifest.xml','-I',android,build/'resources.zip')
classes=build/'classes';shutil.rmtree(classes,ignore_errors=True);classes.mkdir()
run(jdk/'bin/javac','-source','8','-target','8','-classpath',android,'-d',classes,*sorted((root/'src').rglob('*.java')))
run(jdk/'bin/jar','cf',build/'classes.jar','-C',classes,'.')
run(tools/'d8','--lib',android,'--min-api','26','--output',build,build/'classes.jar')
with zipfile.ZipFile(build/'unsigned.apk','a') as package:package.write(build/'classes.dex','classes.dex')
run(tools/'zipalign','-f','4',build/'unsigned.apk',build/'aligned.apk')
key=build/'debug.keystore'
if not key.exists():
 run(jdk/'bin/keytool','-genkeypair','-keystore',key,'-storepass','android','-keypass','android','-alias','androiddebugkey','-dname','CN=TV Starter Debug','-keyalg','RSA','-keysize','2048','-validity','10000')
 key.chmod(0o600)
run(tools/'apksigner','sign','--ks',key,'--ks-pass','pass:android','--key-pass','pass:android','--out',build/'TVStarter.apk',build/'aligned.apk')
run(tools/'apksigner','verify',build/'TVStarter.apk')
print('Built and verified',build/'TVStarter.apk')
