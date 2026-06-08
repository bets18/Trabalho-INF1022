import ply.lex as lex

# Dicionário de palavras reservadas
reservadas = {
    'dispositivo': 'DISPOSITIVO',
    'set': 'SET',
    'se': 'SE',
    'entao': 'ENTAO',
    'senao': 'SENAO',
    'ligar': 'LIGAR',
    'desligar': 'DESLIGAR',
    'verificar': 'VERIFICAR',
    'enviar': 'ENVIAR',
    'alerta': 'ALERTA',
    'para': 'PARA',
    'todos': 'TODOS'
}

# Lista de tokens
tokens = [
    'DOISPONTOS', 'LBRACE', 'RBRACE', 'LPAREN', 'RPAREN',
    'COMMA', 'DOT', 'EQUALS', 'AND',
    'GT', 'LT', 'GE', 'LE', 'EQ', 'NE',
    'ID', 'NUM', 'MSG', 'BOOL'
] + list(reservadas.values())

# Tokens simples
t_DOISPONTOS = r':'
t_LBRACE     = r'\{'
t_RBRACE     = r'\}'
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_COMMA      = r','
t_DOT        = r'\.'
t_EQUALS     = r'='
t_AND        = r'&&'

# Operadores relacionais
t_EQ = r'=='
t_NE = r'!='
t_GE = r'>='
t_LE = r'<='
t_GT = r'>'
t_LT = r'<'

# Mensagens de texto (ex: " mensagem ")
def t_MSG(t):
    r'\"([^\\\n]|(\\.))*?\"'
    # Remove as aspas da string lida
    t.value = t.value[1:-1]
    return t

# Identificadores e palavras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in ('True', 'False'):
        t.type = 'BOOL'
        t.value = True if t.value == 'True' else False
    else:
        # Checa se é uma palavra reservada, senão é um ID normal (como nome de dispositivo)
        t.type = reservadas.get(t.value, 'ID')    
    return t

# Números (inteiros não negativos)
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Controla o número das linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignora espaços e tabs
t_ignore  = ' \t\r'

# Tratamento de erros
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

# Constrói o lexer
lexer = lex.lex()
