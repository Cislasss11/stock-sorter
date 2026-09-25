import os
import subprocess

os.environ['PATH'] = r'C:\Program Files\Git\bin;C:\Program Files\Git\cmd;C:\Program Files\GitHub CLI;' + os.environ.get('PATH', '')

repo_path = r'C:\Users\cesar\Desktop\Proyecto_Stock'
os.chdir(repo_path)

for f in ['check_auth.py']:
    path = os.path.join(repo_path, f)
    if os.path.exists(path):
        os.remove(path)
        print(f"Eliminado: {f}")

subprocess.run(['git', 'add', '-A'], check=True)
subprocess.run(['git', 'commit', '-m', 'Remove check_auth.py'], check=True)
subprocess.run(['git', 'push'], capture_output=True, text=True, timeout=30)
print("\nFIN.")
