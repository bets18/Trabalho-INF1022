import ply.yacc as yacc
from lexico import tokens

# Regras de precedência para evitar conflitos de shift/reduce (como no "senao")
precedence = (
    ('right', 'SENAO'),
    ('left', 'AND'),
    ('left', 'EQ', 'NE', 'GT', 'LT', 'GE', 'LE')
)

def p_programa(p):
    'PROGRAM : DEVICES CMDS'
    p[0] = ('programa', p[1], p[2])

def p_dispositivos_multiplos(p):
    'DEVICES : DEVICE DEVICES'
    p[0] = [p[1]] + p[2]

def p_dispositivos_unico(p):
    'DEVICES : DEVICE'
    p[0] = [p[1]]

def p_dispositivo_simples(p):
    'DEVICE : DISPOSITIVO opt_doispontos LBRACE namedevice RBRACE'
    p[0] = ('dispositivo', p[4], None)

def p_dispositivo_obs(p):
    'DEVICE : DISPOSITIVO opt_doispontos LBRACE namedevice COMMA observation RBRACE'
    p[0] = ('dispositivo', p[4], p[6])

def p_opt_doispontos(p):
    '''opt_doispontos : DOISPONTOS
                      | empty'''
    pass

def p_namedevice(p):
    'namedevice : ID'
    if not p[1].isalpha():
        print(f"Aviso: namedevice '{p[1]}' deveria conter apenas letras (linha {p.lineno(1)}).")
    p[0] = p[1]

def p_observation(p):
    'observation : ID'
    p[0] = p[1]

# Torna o ponto (.) opcional para tolerar todos os exemplos mal formatados do professor
def p_comandos(p):
    '''CMDS : CMD DOT CMDS
            | CMD CMDS
            | DOT CMDS
            | CMD DOT
            | CMD
            | DOT'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3] if p[1] else p[3]
    elif len(p) == 3:
        if p[1] == '.':
            p[0] = p[2]
        elif p[2] == '.':
            p[0] = [p[1]] if p[1] else []
        else:
            p[0] = [p[1]] + p[2] if p[1] else p[2]
    elif len(p) == 2:
        if p[1] == '.':
            p[0] = []
        else:
            p[0] = [p[1]] if p[1] else []

def p_comando_acao(p):
    '''CMD : ATTRIB
           | OBSACT
           | ACT'''
    p[0] = p[1]

def p_comando_vazio(p):
    'CMD : empty'
    p[0] = None

def p_vazio(p):
    'empty :'
    pass

def p_atribuicao_variavel(p):
    'ATTRIB : SET observation EQUALS VAR'
    p[0] = ('atribuicao', p[2], p[4])

def p_atribuicao_exec(p):
    'ATTRIB : SET observation EQUALS ACT_EXECUTE'
    p[0] = ('atribuicao_exec', p[2], p[4])

def p_atribuicao_tupla(p):
    'ATTRIB : SET LBRACE namedevice COMMA observation RBRACE EQUALS VAR'
    p[0] = ('atribuicao_tupla', p[3], p[5], p[8])

def p_obsact_se(p):
    'OBSACT : SE OBS ENTAO CMDS'
    p[0] = ('se_entao', p[2], p[4], [])

def p_obsact_se_senao(p):
    'OBSACT : SE OBS ENTAO CMDS SENAO CMDS'
    p[0] = ('se_entao', p[2], p[4], p[6])

def p_obs_base(p):
    '''OBS_BASE : observation oplogic VAR
                | ACT_EXECUTE oplogic VAR'''
    if isinstance(p[1], str):
        p[0] = ('observacao', p[1], p[2], p[3])
    else:
        p[0] = ('obs_execucao', p[1], p[2], p[3])

def p_obs_and(p):
    '''OBS : OBS_BASE
           | OBS_BASE AND OBS'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('obs_e', p[1], p[3])

def p_oplogic(p):
    '''oplogic : GT
               | LT
               | GE
               | LE
               | EQ
               | NE'''
    p[0] = p[1]

def p_var(p):
    '''VAR : NUM
           | BOOL'''
    if isinstance(p[1], bool):
        p[0] = ('booleano', p[1])
    else:
        p[0] = ('numero', p[1])

def p_act(p):
    '''ACT : ACT_EXECUTE
           | ACT_ALERT'''
    p[0] = p[1]

def p_action(p):
    '''ACTION : LIGAR
              | DESLIGAR
              | VERIFICAR'''
    p[0] = p[1]

def p_acao_exec_sem_parenteses(p):
    'ACT_EXECUTE : ACTION namedevice'
    p[0] = ('acao_executar', p[1], p[2])

def p_acao_exec_com_parenteses(p):
    'ACT_EXECUTE : ACTION LPAREN namedevice RPAREN'
    p[0] = ('acao_executar', p[1], p[3])

def p_acao_alerta_base(p):
    '''ACT_ALERT_BASE : ENVIAR ALERTA MSG
                      | ENVIAR ALERTA LPAREN MSG RPAREN
                      | ENVIAR ALERTA MSG COMMA observation
                      | ENVIAR ALERTA LPAREN MSG COMMA observation RPAREN'''
    if len(p) == 4:
        p[0] = ('alerta_base', p[3], None)
    elif len(p) == 6 and p[3] == '(':
        p[0] = ('alerta_base', p[4], None)
    elif len(p) == 6 and p[4] == ',':
        p[0] = ('alerta_base', p[3], p[5])
    elif len(p) == 8:
        p[0] = ('alerta_base', p[4], p[6])

def p_acao_alerta_simples(p):
    'ACT_ALERT : ACT_ALERT_BASE namedevice'
    p[0] = ('acao_alerta', p[1][1], p[1][2], [p[2]])

def p_acao_alerta_broadcast(p):
    'ACT_ALERT : ACT_ALERT_BASE PARA TODOS DOISPONTOS DEVICE_LIST'
    p[0] = ('acao_alerta', p[1][1], p[1][2], p[5])

def p_lista_dispositivos_multipla(p):
    'DEVICE_LIST : namedevice COMMA DEVICE_LIST'
    p[0] = [p[1]] + p[3]

def p_lista_dispositivos_unica(p):
    'DEVICE_LIST : namedevice'
    p[0] = [p[1]]

def p_error(p):
    if p:
        print(f"Erro de sintaxe próximo ao token '{p.value}' (tipo: {p.type}) na linha {p.lineno}")
    else:
        print("Erro de sintaxe: Fim de arquivo inesperado")

parser = yacc.yacc()
