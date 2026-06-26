from sly import Parser
from obsact_lexer import ObsActLexer

class ObsActParser(Parser):
    # O Parser é a segunda etapa: ele pega a lista de tokens do Lexer e cria a Árvore Sintática (AST).
    # Associando os tokens definidos no Lexer para que o Parser conheça as "pecinhas".
    tokens = ObsActLexer.tokens

    # A regra principal (program). Um programa é feito de dispositivos seguidos de comandos.
    @_('devices cmds')
    def program(self, p):
        # Aqui a gente começa a montar a Árvore Sintática Abstrata (AST).
        # Retornamos uma tupla: o tipo do nó ('program') e seus "filhos" (a lista de devices e a lista de cmds)
        return ('program', p.devices, p.cmds)

    # Regra para ler um bloco de dispositivos. Como pode ter mais de um, a gente usa recursividade.
    @_('device devices')
    def devices(self, p):
        # Junta o dispositivo atual com o resto da lista que foi processada
        return [p.device] + p.devices

    @_('device')
    def devices(self, p):
        # Caso base da recursão: se tiver só um dispositivo, retorna uma lista com ele
        return [p.device]

    # Regra pra definir um dispositivo simples. Ex: dispositivo: { Luz }
    @_('DISPOSITIVO DOISPONTOS ACHAVES ID FCHAVES')
    def device(self, p):
        # Retorna o nó 'device' passando o ID do dispositivo
        return ('device', p.ID)

    # Regra pra dispositivo que contém uma variável. Ex: dispositivo: { Termometro, temperatura }
    @_('DISPOSITIVO DOISPONTOS ACHAVES ID VIRGULA ID FCHAVES')
    def device(self, p):
        # Quando a regra tem mais de um mesmo token (no caso, dois IDs), 
        # o SLY os indexa automaticamente para a gente conseguir pegar o valor de cada um.
        return ('device', p.ID0, p.ID1)

    # Regra para processar múltiplos comandos. Mesma lógica de recursividade dos devices.
    @_('cmd PONTO cmds')
    def cmds(self, p):
        return [p.cmd] + p.cmds

    @_('cmd PONTO')
    def cmds(self, p):
        return [p.cmd]

    # Um comando genérico (cmd) pode ser uma atribuição, uma verificação condicional (obsact) ou uma ação direta (act)
    @_('attrib')
    def cmd(self, p):
        return p.attrib

    @_('obsact')
    def cmd(self, p):
        return p.obsact

    @_('act')
    def cmd(self, p):
        return p.act

    # Atribuição. Ex: set temperatura = 30
    @_('SET ID IGUAL var')
    def attrib(self, p):
        # Retorna nó 'attrib' com o ID da variável e o valor novo
        return ('attrib', p.ID, p.var)

    # Estruturas condicionais (se / senao)
    @_('SE obs ENTAO cmds')
    def obsact(self, p):
        # Condicional simples (tipo if do C)
        return ('if', p.obs, p.cmds)

    @_('SE obs ENTAO cmds SENAO cmds')
    def obsact(self, p):
        # Condicional completa (tipo if/else). 
        # Novamente, o SLY indexa 'cmds' como p.cmds0 (bloco do ENTÃO) e p.cmds1 (bloco do SENÃO).
        return ('if_else', p.obs, p.cmds0, p.cmds1)

    # Condição que é verificada dentro do "se". Ex: temperatura > 30
    @_('ID oplogic var')
    def obs(self, p):
        # Nó de condição simples
        return ('condition', p.ID, p.oplogic, p.var)

    @_('ID oplogic var E_LOGICO obs')
    def obs(self, p):
        # Nó de condição composta com o operador E LÓGICO (&&)
        return ('condition_and', p.ID, p.oplogic, p.var, p.obs)

    # Regras para os tipos de valores (var) que as variáveis podem assumir
    @_('NUM')
    def var(self, p):
        return ('num', p.NUM)

    @_('TRUE')
    def var(self, p):
        # Passa o booleano de verdade pro Python
        return ('bool', True)

    @_('FALSE')
    def var(self, p):
        return ('bool', False)

    # EXPANSÃO DA GRAMÁTICA: BROADCAST (Enviando pra vários)
    # Lista de dispositivos separada por vírgula
    @_('ID VIRGULA lista_devices')
    def lista_devices(self, p):
        return [p.ID] + p.lista_devices

    @_('ID')
    def lista_devices(self, p):
        return [p.ID]

    # Regras para as Ações (act)
    @_('action ID')
    def act(self, p):
        # Ação direta simples num dispositivo. Ex: ligar Luz
        return ('act', p.action, p.ID)

    @_('ENVIAR ALERTA APARENTESES MSG FPARENTESES ID')
    def act(self, p):
        # Enviar alerta de texto puro pra um dispositivo específico
        return ('alert', p.MSG, p.ID)

    @_('ENVIAR ALERTA APARENTESES MSG VIRGULA ID FPARENTESES ID')
    def act(self, p):
        # Enviar alerta que mostra também o valor de uma variável.
        # ID0 é a variável e ID1 é quem vai receber a mensagem.
        return ('alert_var', p.MSG, p.ID0, p.ID1)

    # EXPANSÃO DA GRAMÁTICA: BROADCAST
    @_('ENVIAR ALERTA APARENTESES MSG FPARENTESES PARA TODOS DOISPONTOS lista_devices')
    def act(self, p):
        return ('alert_broadcast', p.MSG, p.lista_devices)

    # FEATURE EXTRA: Agendamento usando a HORA exata (hh:mm)
    @_('AGENDAR ID HORA')
    def act(self, p):
        return ('agendar', p.ID, p.HORA)

    # Define quais as palavras equivalem às ações simples (para simplificar o act lá de cima)
    @_('LIGAR')
    def action(self, p):
        return 'ligar'

    @_('DESLIGAR')
    def action(self, p):
        return 'desligar'

    @_('VERIFICAR')
    def action(self, p):
        return 'verificar'

    # FEATURE EXTRA: Adicionando ação de FECHAR (como para fechar porta/cortina)
    @_('FECHAR')
    def action(self, p):
        return 'fechar'

    # Tradução dos operadores lógicos para a nossa AST e posterior código C
    @_('MAIOR')
    def oplogic(self, p):
        return '>'

    @_('MENOR')
    def oplogic(self, p):
        return '<'

    @_('MAIORIGUAL')
    def oplogic(self, p):
        return '>='

    @_('MENORIGUAL')
    def oplogic(self, p):
        return '<='

    @_('IGUALIGUAL')
    def oplogic(self, p):
        return '=='

    @_('DIFERENTE')
    def oplogic(self, p):
        return '!='
