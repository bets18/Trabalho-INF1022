import ply.lex as lex

# Lista de tokens necessários para o analisador léxico.
# Você precisará adicionar os outros tokens do trabalho aqui.
tokens = (
    'DISPOSITIVO',
    'DOISPONTOS',
    'LBRACE',
    'RBRACE',
    'NAMEDEVICE',
)

# Regras de expressão regular para tokens simples
t_DOISPONTOS = r':'
t_LBRACE     = r'\{'
t_RBRACE     = r'\}'

# Regra para a palavra-chave "dispositivo"
def t_DISPOSITIVO(t):
    r'dispositivo'
    return t

# Regra para nomes de devices (apenas letras, segundo o enunciado)
def t_NAMEDEVICE(t):
    r'[a-zA-Z]+'
    # Dica: cuidado com conflitos com outras palavras-chave (como "se", "entao", "set")!
    return t

# Define uma regra para rastrear números de linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Caracteres a serem ignorados (espaços e tabs)
t_ignore  = ' \t\r'

# Regra de tratamento de erros léxicos
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

# Constrói o lexer
lexer = lex.lex()
