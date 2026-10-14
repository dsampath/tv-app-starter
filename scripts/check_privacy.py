"""Scan Git tracked files; complementary to secret scanning and manual media review."""
from pathlib import Path
import re, subprocess, sys
root = Path(__file__).resolve().parents[1]
files = subprocess.check_output(['git','ls-files','-z'], cwd=root).decode().split('\0')
patterns = {
 'local path': r'/Users/[^/\s]+|/home/[^/\s]+',
 'private address': r'\b(?:192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+|172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+)(?::\d+)?\b',
 'tailnet': r'[a-z0-9.-]+\.ts\.net',
 'credential': r'(?i)-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bsk-(?:proj-)?[a-zA-Z0-9_-]{20,}|\b(?:ghp|github_pat)_[a-zA-Z0-9_]{20,}|\bAIza[a-zA-Z0-9_-]{30,}',
 'signing identity': r'DEVELOPMENT_TEAM\s*=|[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
}
forbidden = {'.keystore','.jks','.p12','.mobileprovision','.log','.apk','.aab'}
failures = []
for name in filter(None, files):
 path = root / name
 if path.is_symlink(): continue
 if path.suffix in forbidden or path.name == '.env' or 'xcuserdata' in path.parts:
  failures.append((name, 'private/generated file')); continue
 if name == 'scripts/check_privacy.py': continue
 try: data = path.read_text()
 except UnicodeDecodeError: continue
 for label, pattern in patterns.items():
  if re.search(pattern, data): failures.append((name,label))
for name,label in failures: print(f'{name}: {label}')
print(f'Privacy scan: {len(files)-1} tracked entries, {len(failures)} issues. Media needs visual review.')
sys.exit(bool(failures))
