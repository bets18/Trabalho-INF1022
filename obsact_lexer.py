from sly import Lexer

class ObsActLexer(Lexer):
    # Conjunto de todos os tokens da linguagem
    tokens = {
        # Palavras Reservadas
        DISPOSITIVO, SET, SE, ENTAO, SENAO, LIGAR, DESLIGAR,
        VERIFICAR, ENVIAR, ALERTA, PARA, TODOS, TRUE, FALSE,
        
        # FEATURE EXTRA: Tokens de Agendamento, Fechar Cortina e Hora
        AGENDAR, FECHAR, HORA,
        
        # Operadores e Símbolos
        IGUALIGUAL, DIFERENTE, MAIORIGUAL, MENORIGUAL, E_LOGICO,
        MAIOR, MENOR, IGUAL, PONTO, DOISPONTOS, VIRGULA,
        APARENTESES, FPARENTESES, ACHAVES, FCHAVES,
        
        # Identificadores e Literais
        ID, NUM, MSG
    }

    # Ignora espaços em branco, tabs e quebras de linha
    ignore = ' \t\n'

    # Definição dos tokens de símbolos (operadores e pontuações) usando Regex.
    # A ordem importa: símbolos compostos vêm primeiro para evitar conflito com os simples.
    IGUALIGUAL = r'=='
    DIFERENTE  = r'!='
    MAIORIGUAL = r'>='
    MENORIGUAL = r'<='
    E_LOGICO   = r'&&'
    
    MAIOR       = r'>'
    MENOR       = r'<'
    IGUAL       = r'='
    PONTO       = r'\.'
    DOISPONTOS  = r':'
    VIRGULA     = r','
    APARENTESES = r'\('
    FPARENTESES = r'\)'
    ACHAVES     = r'\{'
    FCHAVES     = r'\}'

    # Token genérico para Identificadores (começa com letra, seguido de letras, números ou underscore)
    ID = r'[a-zA-Z][a-zA-Z0-9_]*'

    # Remapeamento (special cases) do token ID para as palavras reservadas da linguagem
    ID['dispositivo'] = DISPOSITIVO
    ID['set']         = SET
    ID['se']          = SE
    ID['entao']       = ENTAO
    ID['senao']       = SENAO
    ID['ligar']       = LIGAR
    ID['desligar']    = DESLIGAR
    ID['verificar']   = VERIFICAR
    ID['enviar']      = ENVIAR
    ID['alerta']      = ALERTA
    ID['para']        = PARA
    ID['todos']       = TODOS
    ID['True']        = TRUE
    ID['False']       = FALSE

    # FEATURE EXTRA: Agendamento e Fechar
    ID['agendar']     = AGENDAR
    ID['fechar']      = FECHAR

    # FEATURE EXTRA: Token de Hora (hh:mm)
    @_(r'\d{2}:\d{2}')
    def HORA(self, t):
        return t

    # Token de Números com função para converter o valor de string para inteiro
    @_(r'\d+')
    def NUM(self, t):
        t.value = int(t.value)
        return t

    # Token de Strings/Mensagens com função para remover as aspas em volta da string
    @_(r'"[^"]*"')
    def MSG(self, t):
        t.value = t.value[1:-1]
        return t

    # Função de tratamento de erros
    def error(self, t):
        print(f"Erro Léxico: caractere {t.value[0]} na linha {self.lineno}")
        self.index += 1
