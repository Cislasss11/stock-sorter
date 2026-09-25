import os
import subprocess

os.environ['PATH'] = r'C:\Program Files\Git\bin;C:\Program Files\Git\cmd;C:\Program Files\GitHub CLI;' + os.environ.get('PATH', '')
os.environ['PYTHONPATH'] = r'C:\Users\cesar\AppData\Roaming\Python\Python312\site-packages'

repo_path = r'C:\Users\cesar\Desktop\Proyecto_Stock'
os.chdir(repo_path)

# Configure git identity
print("[1/6] Configurando identidad de git...")
subprocess.run(['git', 'config', '--global', 'user.email', 'cesar@cesar.local'], check=True)
subprocess.run(['git', 'config', '--global', 'user.name', 'Cesar'], check=True)
print("   -> Email: cesar@cesar.local")
print("   -> Nombre: Cesar")

# Initialize git
print("\n[2/6] Inicializando repositorio...")
subprocess.run(['git', 'init'], check=True)
subprocess.run(['git', 'add', '.'], check=True)
subprocess.run(['git', 'commit', '-m', 'Initial commit: stock sorter tool'], check=True)
print("   -> Commit inicial creado")

# Check auth
print("\n[3/6] Verificando autenticacion con GitHub...")
auth = subprocess.run(['gh', 'auth', 'status'], capture_output=True, text=True)
if auth.returncode != 0:
    print("   -> NO autenticado con GitHub.")
    print("   -> Abre una terminal/PowerShell y ejecuta:")
    print("      gh auth login")
    print("   -> Selecciona GitHub.com, tu cuenta, y el metodo de autenticacion")
    print("   -> Despues vuelve aqui y vuelve a ejecutar este script")
    # Stop here
    print("\n[PENDIENTE] Autenticacion requerida. Abre otra terminal y ejecuta:")
    print("   gh auth login")
    raise SystemExit(0)
else:
    print("   -> Autenticado correctamente")

# Create repo
print("\n[4/6] Creando repositorio en GitHub...")
result = subprocess.run([
    'gh', 'repo', 'create', 'stock-sorter',
    '--public', '--source', repo_path,
    '--remote', 'origin', '--push'
], capture_output=True, text=True)

if result.returncode == 0:
    print("   -> Repositorio creado y codeudido!")
    print(f"   -> URL: https://github.com/stock-sorter")
else:
    print(f"   -> Error creando: {result.stderr[:200]}")
    # Try to add remote manually and push
    print("\n   -> Intentando push manual...")
    subprocess.run(['git', 'remote', 'add', 'origin', 'https://github.com/<usuario>/stock-sorter.git'], check=False)
    print("\n[PENDIENTE] Reemplaza <usuario> con tu nombre de usuario de GitHub")
    print("   Ejecuta: gh auth login")
    print("   Ejecuta: gh repo create stock-sorter --public")
    print("   Ejecuta: git push -u origin main")

# Summary
print("\n[5/6] Archivos en el repositorio:")
for f in os.listdir(repo_path):
    if not f.startswith('.'):
        print(f"   - {f}")

print("\n[6/6] ¡Listo! Revisa https://github.com para ver tu repositorio.")
