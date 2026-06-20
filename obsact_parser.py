from sly import Parser
from obsact_lexer import ObsActLexer

class ObsActParser(Parser):
    # Associando os tokens definidos no Lexer para que o Parser possa usá-los
    tokens = ObsActLexer.tokens

    # program : devices cmds
    @_('devices cmds')
    def program(self, p):
        # A Árvore Sintática Abstrata (AST) começa aqui.
        # Retornamos uma tupla cujo primeiro elemento é o nome do nó ('program')
        # seguido pelas ramificações que contêm a lista de dispositivos e os comandos.
        return ('program', p.devices, p.cmds)

    # devices : device devices | device
    @_('device devices')
    def devices(self, p):
        # Regra recursiva: agrupa o dispositivo atual com o resto da lista de dispositivos
        return [p.device] + p.devices

    @_('device')
    def devices(self, p):
        # Caso base da recursão: retorna apenas uma lista com o primeiro dispositivo
        return [p.device]

    # device : DISPOSITIVO DOISPONTOS ACHAVES ID FCHAVES
    @_('DISPOSITIVO DOISPONTOS ACHAVES ID FCHAVES')
    def device(self, p):
        # Retorna o nó 'device' com um único ID associado
        return ('device', p.ID)

    # device : DISPOSITIVO DOISPONTOS ACHAVES ID VIRGULA ID FCHAVES
    @_('DISPOSITIVO DOISPONTOS ACHAVES ID VIRGULA ID FCHAVES')
    def device(self, p):
        # Quando há elementos repetidos no SLY (como o ID aqui), ele os indexa 
        # automaticamente, podendo ser acessados por p.ID0, p.ID1, etc.
        return ('device', p.ID0, p.ID1)

    # cmds : cmd PONTO cmds | cmd PONTO
    @_('cmd PONTO cmds')
    def cmds(self, p):
        # Adiciona o comando atual na lista com os próximos comandos
        return [p.cmd] + p.cmds

    @_('cmd PONTO')
    def cmds(self, p):
        # Caso base da lista de comandos
        return [p.cmd]

    # cmd : attrib | obsact | act
    @_('attrib')
    def cmd(self, p):
        return p.attrib

    @_('obsact')
    def cmd(self, p):
        return p.obsact

    @_('act')
    def cmd(self, p):
        return p.act

    # attrib : SET ID IGUAL var
    @_('SET ID IGUAL var')
    def attrib(self, p):
        # Nó da AST de atribuição (ex: set temp = 30)
        return ('attrib', p.ID, p.var)

    # obsact : SE obs ENTAO cmds | SE obs ENTAO cmds SENAO cmds
    @_('SE obs ENTAO cmds')
    def obsact(self, p):
        # Estrutura condicional simples (if)
        return ('if', p.obs, p.cmds)

    @_('SE obs ENTAO cmds SENAO cmds')
    def obsact(self, p):
        # Condicional completa (if/else). SLY indexa 'cmds' como cmds0 (no ENTÃO) e cmds1 (no SENÃO).
        return ('if_else', p.obs, p.cmds0, p.cmds1)

    # obs : ID oplogic var | ID oplogic var E_LOGICO obs
    @_('ID oplogic var')
    def obs(self, p):
        # Nó de condição de observação simples
        return ('condition', p.ID, p.oplogic, p.var)

    @_('ID oplogic var E_LOGICO obs')
    def obs(self, p):
        # Nó de condição composta com o E LÓGICO (&&)
        return ('condition_and', p.ID, p.oplogic, p.var, p.obs)

    # var : NUM | TRUE | FALSE
    @_('NUM')
    def var(self, p):
        # Retorna o tipo de valor numérico.
        return ('num', p.NUM)

    @_('TRUE')
    def var(self, p):
        # Retorna o valor booleano puro (convertido do léxico)
        return ('bool', True)

    @_('FALSE')
    def var(self, p):
        return ('bool', False)

    # EXPANSÃO DA GRAMÁTICA: BROADCAST
    @_('ID VIRGULA lista_devices')
    def lista_devices(self, p):
        return [p.ID] + p.lista_devices

    @_('ID')
    def lista_devices(self, p):
        return [p.ID]

    # act : action ID | ENVIAR ALERTA APARENTESES MSG FPARENTESES ID | ENVIAR ALERTA APARENTESES MSG VIRGULA ID FPARENTESES ID
    @_('action ID')
    def act(self, p):
        # Uma ação em um dispositivo, como 'ligar luz'
        return ('act', p.action, p.ID)

    @_('ENVIAR ALERTA APARENTESES MSG FPARENTESES ID')
    def act(self, p):
        # Ação para enviar alerta contendo só texto para um determinado destinatário (ID)
        return ('alert', p.MSG, p.ID)

    @_('ENVIAR ALERTA APARENTESES MSG VIRGULA ID FPARENTESES ID')
    def act(self, p):
        # Alerta contendo uma variável extra dentro do alerta. 
        # O SLY indexa os IDs: ID0 (variável a ser avaliada), ID1 (destinatário final)
        return ('alert_var', p.MSG, p.ID0, p.ID1)

    # EXPANSÃO DA GRAMÁTICA: BROADCAST
    @_('ENVIAR ALERTA APARENTESES MSG FPARENTESES PARA TODOS DOISPONTOS lista_devices')
    def act(self, p):
        return ('alert_broadcast', p.MSG, p.lista_devices)

    # FEATURE EXTRA: Adicionando ação de agendar com HORA
    @_('AGENDAR ID HORA')
    def act(self, p):
        return ('agendar', p.ID, p.HORA)

    # action : LIGAR | DESLIGAR | VERIFICAR
    @_('LIGAR')
    def action(self, p):
        return 'ligar'

    @_('DESLIGAR')
    def action(self, p):
        return 'desligar'

    @_('VERIFICAR')
    def action(self, p):
        return 'verificar'

    # FEATURE EXTRA: Adicionando ação de FECHAR
    @_('FECHAR')
    def action(self, p):
        return 'fechar'

    # oplogic : MAIOR | MENOR | MAIORIGUAL | MENORIGUAL | IGUALIGUAL | DIFERENTE
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
