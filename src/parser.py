import ply.yacc as yacc

# Importa os tokens definidos no lexer
from lexer import tokens

# Regras da gramática (Parser)
# O ply usa o formato p_nomedaregra e a docstring para definir a gramática.

def p_program(p):
    'PROGRAM : DEVICES'
    p[0] = p[1]

# Como um PROGRAM pode ter vários DEVICES, criamos uma regra recursiva
# Por enquanto deixei apenas uma regra de DEVICE simples para você continuar.
def p_devices_single(p):
    'DEVICES : DEVICE'
    p[0] = [p[1]]

def p_device(p):
    'DEVICE : DISPOSITIVO DOISPONTOS LBRACE NAMEDEVICE RBRACE'
    # Salva na árvore de sintaxe o que foi encontrado
    p[0] = ('device', p[4])

# Regra para tratamento de erros sintáticos
def p_error(p):
    if p:
        print(f"Erro de sintaxe próximo ao token '{p.value}' (tipo: {p.type}) na linha {p.lineno}")
    else:
        print("Erro de sintaxe: Fim de arquivo inesperado")

# Constrói o parser
parser = yacc.yacc()
