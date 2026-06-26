from obsact_lexer import ObsActLexer
from obsact_parser import ObsActParser
from obsact_transpiler import ObsActTranspiler

def compilar():
    # Fase Inicial: Lê o código escrito na nossa linguagem (arquivo .obsact)
    try:
        # Abrimos o arquivo contendo nosso código fonte
        with open('teste.obsact', 'r', encoding='utf-8') as f:
            texto = f.read()
    except FileNotFoundError:
        print("Erro: Crie o arquivo teste.obsact na mesma pasta!")
        return

    # Instancia (liga) as três máquinas que fazem o compilador funcionar
    lexer = ObsActLexer()
    parser = ObsActParser()
    transpiler = ObsActTranspiler()

    print("Iniciando a compilação...")
    
    # O coração do compilador: o pipeline de tradução (Texto -> Tokens -> AST -> Código C)
    
    # O Lexer quebra o texto puro em Tokens (palavras que a linguagem conhece)
    tokens = lexer.tokenize(texto)
    
    # O Parser recebe os tokens e monta a Árvore Sintática (AST) baseada nas regras gramaticais
    ast = parser.parse(tokens)
    
    # Se a AST for montada com sucesso (ou seja, não teve erro de sintaxe)
    if ast:
        # O Transpiler pega a Árvore (AST) e a percorre, traduzindo cada nó para código em C
        codigo_c = transpiler.transpile(ast)
        
        # Finalização: Salva o código C gerado no arquivo saida.c
        with open('saida.c', 'w', encoding='utf-8') as f:
            f.write(codigo_c)
        print("\nSucesso! \nO arquivo saida.c foi gerado.\n")
    else:
        # Se algo falhou no Parser (erro de sintaxe), a compilação para aqui.
        print("A compilação falhou. Verifique se digitou o código ObsAct certinho.")

if __name__ == '__main__':
    # Só roda a compilação se a gente executar esse script diretamente (pelo terminal)
    compilar()