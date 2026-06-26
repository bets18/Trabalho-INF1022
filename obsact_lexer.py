from sly import Lexer

class ObsActLexer(Lexer):
    # Aqui a gente define todos os tokens (palavras e símbolos) que a nossa linguagem entende.
    # O Lexer é a primeira etapa: ele lê o texto puro e "quebra" nessas pecinhas chamadas tokens.
    tokens = {
        # Palavras Reservadas da nossa linguagem (comandos base)
        DISPOSITIVO, SET, SE, ENTAO, SENAO, LIGAR, DESLIGAR,
        VERIFICAR, ENVIAR, ALERTA, PARA, TODOS, TRUE, FALSE,
        
        # FEATURE EXTRA: Adicionamos comandos novos como agendar e fechar coisas, e lidar com horários.
        AGENDAR, FECHAR, HORA,
        
        # Operadores matemáticos, lógicos e símbolos de pontuação
        IGUALIGUAL, DIFERENTE, MAIORIGUAL, MENORIGUAL, E_LOGICO,
        MAIOR, MENOR, IGUAL, PONTO, DOISPONTOS, VIRGULA,
        APARENTESES, FPARENTESES, ACHAVES, FCHAVES,
        
        # Identificadores (nomes de variáveis/dispositivos) e Tipos de valores (números, textos de mensagem)
        ID, NUM, MSG
    }

    # Ignora espaços em branco, "tabs" e quebras de linha para não poluir os tokens
    ignore = ' \t\n'

    # Definição dos tokens de símbolos usando Regex (Expressões Regulares).
    # A ordem importa muito! Símbolos compostos (como '==' ou '>=') vêm primeiro, senão o Lexer pegaria só o '=' ou '>' e daria erro.
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

    # Token genérico para Identificadores (nomes). Começa com letra, seguido de letras, números ou underline.
    ID = r'[a-zA-Z][a-zA-Z0-9_]*'

    # Aqui é um truque legal: em vez de criar um Regex pra cada palavra reservada, 
    # a gente usa o token 'ID' para capturar qualquer palavra, e depois faz um "remapeamento" para o token certo.
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

    # FEATURE EXTRA: Mapeando os comandos extras
    ID['agendar']     = AGENDAR
    ID['fechar']      = FECHAR

    # FEATURE EXTRA: Token de Hora no formato exato hh:mm (dois números, dois pontos, dois números)
    @_(r'\d{2}:\d{2}')
    def HORA(self, t):
        return t

    # Quando achamos números (Regex \d+), convertemos logo o valor (que era string) para inteiro
    @_(r'\d+')
    def NUM(self, t):
        t.value = int(t.value)
        return t

    # Quando achamos uma mensagem (texto entre aspas duplas), removemos as aspas do começo e do fim
    @_(r'"[^"]*"')
    def MSG(self, t):
        t.value = t.value[1:-1]
        return t

    # Função de tratamento de erros, caso o Lexer encontre um caractere que não faz parte das nossas regras
    def error(self, t):
        print(f"Erro Léxico: caractere {t.value[0]} na linha {self.lineno}")
        self.index += 1
