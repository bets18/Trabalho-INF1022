class Gerador:
    def __init__(self):
        self.codigo = []
        self.nivel_indentacao = 0

    def adicionar_linha(self, linha):
        if linha.strip() == "":
            self.codigo.append("")
        else:
            self.codigo.append("    " * self.nivel_indentacao + linha)

    def transpile(self, ast):
        # Funções base pedidas no enunciado
        self.adicionar_linha("def ligar(namedevice):")
        self.nivel_indentacao += 1
        self.adicionar_linha('print(f"{namedevice} ligado!")')
        self.adicionar_linha('return 1')
        self.nivel_indentacao -= 1
        self.adicionar_linha("")

        self.adicionar_linha("def desligar(namedevice):")
        self.nivel_indentacao += 1
        self.adicionar_linha('print(f"{namedevice} desligado!")')
        self.adicionar_linha('return 0')
        self.nivel_indentacao -= 1
        self.adicionar_linha("")

        self.adicionar_linha("def verificar(namedevice):")
        self.nivel_indentacao += 1
        self.adicionar_linha('print(f"{namedevice} está ligado.")')
        self.adicionar_linha('return 1 # Pode ser 0 dependendo da lógica')
        self.nivel_indentacao -= 1
        self.adicionar_linha("")

        self.adicionar_linha("def alerta(namedevice, msg, var=None):")
        self.nivel_indentacao += 1
        self.adicionar_linha('print(f"{namedevice} recebeu o alerta:\\n")')
        self.adicionar_linha('if var is not None:')
        self.adicionar_linha('    print(f"{msg} {var}")')
        self.adicionar_linha('else:')
        self.adicionar_linha('    print(msg)')
        self.nivel_indentacao -= 1
        self.adicionar_linha("")

        # Parse AST: ('programa', dispositivos, comandos)
        if not ast or ast[0] != 'programa':
            return ""

        dispositivos = ast[1]
        comandos = ast[2]

        observacoes = set()
        for disp in dispositivos:
            if disp[2]: # se tem variável de observação
                observacoes.add(disp[2])

        # Inicializa observações com 0 (regra 1.4 do enunciado)
        if observacoes:
            for obs in observacoes:
                self.adicionar_linha(f"{obs} = 0")
            self.adicionar_linha("")

        self.visitar_comandos(comandos)

        return "\n".join(self.codigo)

    def visitar_comandos(self, comandos):
        for cmd in comandos:
            if cmd is None:
                continue
            self.visitar_comando(cmd)

    def visitar_comando(self, cmd):
        tipo_comando = cmd[0]
        if tipo_comando == 'atribuicao':
            # ('atribuicao', observacao, variavel)
            valor = self.visitar_variavel(cmd[2])
            self.adicionar_linha(f"{cmd[1]} = {valor}")
        elif tipo_comando == 'atribuicao_exec':
            # ('atribuicao_exec', observacao, acao_exec)
            valor = self.visitar_acao_exec(cmd[2])
            self.adicionar_linha(f"{cmd[1]} = {valor}")
        elif tipo_comando == 'atribuicao_tupla':
            # ('atribuicao_tupla', dispositivo, observacao, variavel)
            valor = self.visitar_variavel(cmd[3])
            # Em Python vamos atribuir apenas a observação da tupla
            self.adicionar_linha(f"{cmd[2]} = {valor} # ignorando o nome do dispositivo {cmd[1]}")
        elif tipo_comando == 'se_entao':
            # ('se_entao', condicao, cmds_entao, cmds_senao)
            cond = self.visitar_observacao(cmd[1])
            self.adicionar_linha(f"if {cond}:")
            self.nivel_indentacao += 1
            if cmd[2]:
                self.visitar_comandos(cmd[2])
            else:
                self.adicionar_linha("pass")
            self.nivel_indentacao -= 1

            if len(cmd) > 3 and cmd[3]:
                self.adicionar_linha("else:")
                self.nivel_indentacao += 1
                self.visitar_comandos(cmd[3])
                self.nivel_indentacao -= 1
        elif tipo_comando == 'acao_executar':
            valor = self.visitar_acao_exec(cmd)
            self.adicionar_linha(valor)
        elif tipo_comando == 'acao_alerta':
            # ('acao_alerta', msg, observacao, lista_dispositivos)
            msg = cmd[1]
            obs = cmd[2]
            lista_disp = cmd[3]
            for disp in lista_disp:
                if obs:
                    self.adicionar_linha(f"alerta('{disp}', '{msg}', {obs})")
                else:
                    self.adicionar_linha(f"alerta('{disp}', '{msg}')")

    def visitar_variavel(self, var):
        if var[0] == 'numero':
            return str(var[1])
        elif var[0] == 'booleano':
            return "True" if var[1] else "False"

    def visitar_observacao(self, obs):
        if obs[0] == 'observacao':
            # ('observacao', nome_obs, operador, variavel)
            valor = self.visitar_variavel(obs[3])
            return f"{obs[1]} {obs[2]} {valor}"
        elif obs[0] == 'obs_execucao':
            # ('obs_execucao', acao_exec, operador, variavel)
            str_exec = self.visitar_acao_exec(obs[1])
            valor = self.visitar_variavel(obs[3])
            return f"{str_exec} {obs[2]} {valor}"
        elif obs[0] == 'obs_e':
            esquerda = self.visitar_observacao(obs[1])
            direita = self.visitar_observacao(obs[2])
            return f"({esquerda}) and ({direita})"

    def visitar_acao_exec(self, cmd):
        # ('acao_executar', acao, dispositivo)
        return f"{cmd[1]}('{cmd[2]}')"
