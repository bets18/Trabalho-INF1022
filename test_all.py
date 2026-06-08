import os
import subprocess
import glob
import sys

def run_tests():
    test_files = glob.glob(os.path.join('testes', '*.txt'))
    test_files.sort()
    
    success = True
    for test in test_files:
        print(f"\n======================================")
        print(f"Executando teste: {test}")
        print(f"======================================")
        
        result = subprocess.run([sys.executable, 'src/main.py', test], capture_output=True, text=True)
        print(result.stdout)
        
        if result.returncode != 0 or 'Erro' in result.stdout or 'Caractere ilegal' in result.stdout:
            print(f">>> TESTE FALHOU: {test}")
            success = False
            
    if success:
        print("\n>>> TODOS OS TESTES PASSARAM COM SUCESSO!")
    else:
        print("\n>>> ALGUNS TESTES FALHARAM!")

if __name__ == '__main__':
    run_tests()
