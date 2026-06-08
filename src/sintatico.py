import ply.yacc as yacc
from lexico import tokens

# Precedence rules to avoid shift/reduce conflicts
precedence = (
    ('right', 'SENAO'),
    ('left', 'AND'),
    ('left', 'EQ', 'NE', 'GT', 'LT', 'GE', 'LE')
)

def p_program(p):
    'PROGRAM : DEVICES CMDS'
    p[0] = ('program', p[1], p[2])

def p_devices_multiple(p):
    'DEVICES : DEVICE DEVICES'
    p[0] = [p[1]] + p[2]

def p_devices_single(p):
    'DEVICES : DEVICE'
    p[0] = [p[1]]

def p_device_simple(p):
    'DEVICE : DISPOSITIVO opt_doispontos LBRACE namedevice RBRACE'
    p[0] = ('device', p[4], None)

def p_device_obs(p):
    'DEVICE : DISPOSITIVO opt_doispontos LBRACE namedevice COMMA observation RBRACE'
    p[0] = ('device', p[4], p[6])

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

# Make DOT totally optional to tolerate all examples
def p_cmds(p):
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

def p_cmd_action(p):
    '''CMD : ATTRIB
           | OBSACT
           | ACT'''
    p[0] = p[1]

def p_cmd_empty(p):
    'CMD : empty'
    p[0] = None

def p_empty(p):
    'empty :'
    pass

def p_attrib_var(p):
    'ATTRIB : SET observation EQUALS VAR'
    p[0] = ('attrib', p[2], p[4])

def p_attrib_exec(p):
    'ATTRIB : SET observation EQUALS ACT_EXECUTE'
    p[0] = ('attrib_exec', p[2], p[4])

def p_attrib_tuple(p):
    'ATTRIB : SET LBRACE namedevice COMMA observation RBRACE EQUALS VAR'
    p[0] = ('attrib_tuple', p[3], p[5], p[8])

def p_obsact_se(p):
    'OBSACT : SE OBS ENTAO CMDS'
    p[0] = ('if', p[2], p[4], [])

def p_obsact_se_senao(p):
    'OBSACT : SE OBS ENTAO CMDS SENAO CMDS'
    p[0] = ('if', p[2], p[4], p[6])

def p_obs_base(p):
    '''OBS_BASE : observation oplogic VAR
                | ACT_EXECUTE oplogic VAR'''
    if isinstance(p[1], str):
        p[0] = ('obs', p[1], p[2], p[3])
    else:
        p[0] = ('obs_exec', p[1], p[2], p[3])

def p_obs_and(p):
    '''OBS : OBS_BASE
           | OBS_BASE AND OBS'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('obs_and', p[1], p[3])

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
        p[0] = ('bool', p[1])
    else:
        p[0] = ('num', p[1])

def p_act(p):
    '''ACT : ACT_EXECUTE
           | ACT_ALERT'''
    p[0] = p[1]

def p_action(p):
    '''ACTION : LIGAR
              | DESLIGAR
              | VERIFICAR'''
    p[0] = p[1]

def p_act_execute_no_paren(p):
    'ACT_EXECUTE : ACTION namedevice'
    p[0] = ('act_exec', p[1], p[2])

def p_act_execute_paren(p):
    'ACT_EXECUTE : ACTION LPAREN namedevice RPAREN'
    p[0] = ('act_exec', p[1], p[3])

def p_act_alert_base(p):
    '''ACT_ALERT_BASE : ENVIAR ALERTA MSG
                      | ENVIAR ALERTA LPAREN MSG RPAREN
                      | ENVIAR ALERTA MSG COMMA observation
                      | ENVIAR ALERTA LPAREN MSG COMMA observation RPAREN'''
    if len(p) == 4:
        p[0] = ('alert_base', p[3], None)
    elif len(p) == 6 and p[3] == '(':
        p[0] = ('alert_base', p[4], None)
    elif len(p) == 6 and p[4] == ',':
        p[0] = ('alert_base', p[3], p[5])
    elif len(p) == 8:
        p[0] = ('alert_base', p[4], p[6])

def p_act_alert_single(p):
    'ACT_ALERT : ACT_ALERT_BASE namedevice'
    p[0] = ('act_alert', p[1][1], p[1][2], [p[2]])

def p_act_alert_broadcast(p):
    'ACT_ALERT : ACT_ALERT_BASE PARA TODOS DOISPONTOS DEVICE_LIST'
    p[0] = ('act_alert', p[1][1], p[1][2], p[5])

def p_device_list_multiple(p):
    'DEVICE_LIST : namedevice COMMA DEVICE_LIST'
    p[0] = [p[1]] + p[3]

def p_device_list_single(p):
    'DEVICE_LIST : namedevice'
    p[0] = [p[1]]

def p_error(p):
    if p:
        print(f"Erro de sintaxe próximo ao token '{p.value}' (tipo: {p.type}) na linha {p.lineno}")
    else:
        print("Erro de sintaxe: Fim de arquivo inesperado")

parser = yacc.yacc()
