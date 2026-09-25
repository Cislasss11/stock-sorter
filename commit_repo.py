import os
import subprocess

os.environ['PATH'] = r'C:\Program Files\Git\bin;C:\Program Files\Git\cmd;C:\Program Files\GitHub CLI;' + os.environ.get('PATH', '')
os.environ['PYTHONPATH'] = r'C:\Users\cesar\AppData\Roaming\Python\Python312\site-packages'

repo_path = r'C:\Users\cesar\Desktop\Proyecto_Stock'
os.chdir(repo_path)

print("[1/3] Agregando .gitignore...")
subprocess.run(['git', 'add', '.gitignore'], check=True)

print("\n[2/3] Commitando cambios...")
subprocess.run(['git', 'add', '-A'], check=True)
subprocess.run(['git', 'commit', '-m', 'Add .gitignore, remove helper scripts, clean repo'], check=True)

print("\n[3/3] Subiendo a GitHub...")
result = subprocess.run(['git', 'push'], capture_output=True, text=True, timeout=30)
print(f"   stdout: {result.stdout.strip()}")
if result.stderr.strip():
    print(f"   stderr: {result.stderr.strip()[-200:]}")
print(f"   Codigo: {result.returncode}")

if result.returncode == 0:
    print("\n✅ REPOSITORIO ACTUALIZADO EN GITHUB!")
    print("   https://github.com/Cislasss11/stock-sorter")
