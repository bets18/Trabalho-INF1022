import ply.lex as lex

# Reserved words dictionary
reserved = {
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

# List of tokens
tokens = [
    'DOISPONTOS', 'LBRACE', 'RBRACE', 'LPAREN', 'RPAREN',
    'COMMA', 'DOT', 'EQUALS', 'AND',
    'GT', 'LT', 'GE', 'LE', 'EQ', 'NE',
    'ID', 'NUM', 'MSG', 'BOOL'
] + list(reserved.values())

# Simple tokens
t_DOISPONTOS = r':'
t_LBRACE     = r'\{'
t_RBRACE     = r'\}'
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_COMMA      = r','
t_DOT        = r'\.'
t_EQUALS     = r'='
t_AND        = r'&&'

# Relational operators
t_EQ = r'=='
t_NE = r'!='
t_GE = r'>='
t_LE = r'<='
t_GT = r'>'
t_LT = r'<'

# String messages (e.g. " mensagem ")
def t_MSG(t):
    r'\"([^\\\n]|(\\.))*?\"'
    # Remove the quotes
    t.value = t.value[1:-1]
    return t

# Identifiers and reserved words
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in ('True', 'False'):
        t.type = 'BOOL'
        t.value = True if t.value == 'True' else False
    else:
        t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t

# Numbers (inteiros não negativos)
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignore spaces and tabs
t_ignore  = ' \t\r'

# Error handling
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
