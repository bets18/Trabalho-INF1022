from obsact_lexer import ObsActLexer
from obsact_parser import ObsActParser
from obsact_transpiler import ObsActTranspiler

def compilar():
    # 1. Lê o código escrito na nossa linguagem
    try:
        with open('teste.obsact', 'r', encoding='utf-8') as f:
            texto = f.read()
    except FileNotFoundError:
        print("Erro: Crie o arquivo teste.obsact na mesma pasta!")
        return

    # 2. Liga as máquinas
    lexer = ObsActLexer()
    parser = ObsActParser()
    transpiler = ObsActTranspiler()

    print("Iniciando a compilação...")
    
    # 3. Faz a tradução (Texto -> Tokens -> Árvore -> C)
    tokens = lexer.tokenize(texto)
    ast = parser.parse(tokens)
    
    if ast:
        codigo_c = transpiler.transpile(ast)
        
        # 4. Salva o resultado
        with open('saida.c', 'w', encoding='utf-8') as f:
            f.write(codigo_c)
        print("\nSucesso! \nO arquivo saida.c foi gerado.\n")
    else:
        print("A compilação falhou. Verifique se digitou o ObsAct certinho.")

if __name__ == '__main__':
    compilar()