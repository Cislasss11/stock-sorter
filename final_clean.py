import os
import subprocess

os.environ['PATH'] = r'C:\Program Files\Git\bin;C:\Program Files\Git\cmd;C:\Program Files\GitHub CLI;' + os.environ.get('PATH', '')

repo_path = r'C:\Users\cesar\Desktop\Proyecto_Stock'
os.chdir(repo_path)

# Remove the last helper
path = os.path.join(repo_path, 'clean_repo.py')
if os.path.exists(path):
    os.remove(path)
    print("Eliminado: clean_repo.py")

# Also make sure .gitignore excludes clean_repo.py
# Add .gitignore again
subprocess.run(['git', 'add', '-A'], check=True)
subprocess.run(['git', 'commit', '-m', 'Final cleanup'], check=True)
result = subprocess.run(['git', 'push'], capture_output=True, text=True, timeout=30)
print(f"Push: {'OK' if result.returncode == 0 else 'FAILED'}")

# Verify
print("\n=== ARCHIVOS FINALES ===")
for f in sorted(os.listdir(repo_path)):
    if not f.startswith('.'):
        print(f"  {f}")
    elif f.startswith('.') and f != '.git':
        print(f"  .{f}")
