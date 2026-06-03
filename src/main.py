import sys
import os

# Adiciona o diretório atual ao path para importação correta
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from lexer import lexer
from parser import parser

def main():
    # Verifica se o usuário passou um arquivo como argumento
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        
        if not os.path.exists(filepath):
            print(f"Erro: Arquivo '{filepath}' não encontrado.")
            sys.exit(1)
            
        with open(filepath, 'r', encoding='utf-8') as f:
            data = f.read()
            
        print(f"--- Processando arquivo: {filepath} ---")
        
        # Reinicia o número de linhas do lexer antes de fazer o parse
        lexer.lineno = 1
        
        # Executa o analisador sintático, que por sua vez chama o léxico
        ast = parser.parse(data, lexer=lexer)
        
        print("\nÁrvore Sintática Abstrata (AST) Gerada:")
        print(ast)
        
    else:
        print("Modo de uso: python src/main.py <caminho_do_arquivo.txt>")
        print("Por favor, crie um arquivo com seu código ObsAct e passe como argumento.")

if __name__ == '__main__':
    main()
