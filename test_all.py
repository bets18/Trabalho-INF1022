import os
import subprocess
import glob
import sys

def rodar_testes():
    arquivos_teste = glob.glob(os.path.join('testes', '*.txt'))
    arquivos_teste.sort()
    
    sucesso = True
    for teste in arquivos_teste:
        print(f"\n======================================")
        print(f"Executando teste: {teste}")
        print(f"======================================")
        
        resultado = subprocess.run([sys.executable, 'src/main.py', teste], capture_output=True, text=True)
        print(resultado.stdout)
        
        if resultado.returncode != 0 or 'Erro' in resultado.stdout or 'Caractere ilegal' in resultado.stdout:
            print(f">>> TESTE FALHOU: {teste}")
            sucesso = False
            
    if sucesso:
        print("\n>>> TODOS OS TESTES PASSARAM COM SUCESSO!")
    else:
        print("\n>>> ALGUNS TESTES FALHARAM!")

if __name__ == '__main__':
    rodar_testes()
