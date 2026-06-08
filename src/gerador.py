class Gerador:
    def __init__(self):
        self.code = []
        self.indent_level = 0

    def add_line(self, line):
        if line.strip() == "":
            self.code.append("")
        else:
            self.code.append("    " * self.indent_level + line)

    def transpile(self, ast):
        # Base functions
        self.add_line("def ligar(namedevice):")
        self.indent_level += 1
        self.add_line('print(f"{namedevice} ligado!")')
        self.add_line('return 1')
        self.indent_level -= 1
        self.add_line("")

        self.add_line("def desligar(namedevice):")
        self.indent_level += 1
        self.add_line('print(f"{namedevice} desligado!")')
        self.add_line('return 0')
        self.indent_level -= 1
        self.add_line("")

        self.add_line("def verificar(namedevice):")
        self.indent_level += 1
        self.add_line('print(f"{namedevice} está ligado.")')
        self.add_line('return 1 # Pode ser 0 dependendo da lógica')
        self.indent_level -= 1
        self.add_line("")

        self.add_line("def alerta(namedevice, msg, var=None):")
        self.indent_level += 1
        self.add_line('print(f"{namedevice} recebeu o alerta:\\n")')
        self.add_line('if var is not None:')
        self.add_line('    print(f"{msg} {var}")')
        self.add_line('else:')
        self.add_line('    print(msg)')
        self.indent_level -= 1
        self.add_line("")

        # Parse AST: ('program', devices, cmds)
        if not ast or ast[0] != 'program':
            return ""

        devices = ast[1]
        cmds = ast[2]

        observations = set()
        for dev in devices:
            if dev[2]: # has observation
                observations.add(dev[2])

        # Initialize observations to 0
        if observations:
            for obs in observations:
                self.add_line(f"{obs} = 0")
            self.add_line("")

        self.visit_cmds(cmds)

        return "\n".join(self.code)

    def visit_cmds(self, cmds):
        for cmd in cmds:
            if cmd is None:
                continue
            self.visit_cmd(cmd)

    def visit_cmd(self, cmd):
        ctype = cmd[0]
        if ctype == 'attrib':
            # ('attrib', obs, var)
            val = self.visit_var(cmd[2])
            self.add_line(f"{cmd[1]} = {val}")
        elif ctype == 'attrib_exec':
            # ('attrib_exec', obs, act_exec)
            val = self.visit_act_exec(cmd[2])
            self.add_line(f"{cmd[1]} = {val}")
        elif ctype == 'attrib_tuple':
            # ('attrib_tuple', dev, obs, var)
            val = self.visit_var(cmd[3])
            # Em Python, se atribuirmos para o dev e para a observação (como diz no exemplo 4)
            # Mas o dev é só uma string identificadora. Vamos atribuir apenas a observação:
            self.add_line(f"{cmd[2]} = {val} # ignorando {cmd[1]}")
        elif ctype == 'if':
            # ('if', obs_cond, cmds1, cmds2)
            cond = self.visit_obs(cmd[1])
            self.add_line(f"if {cond}:")
            self.indent_level += 1
            if cmd[2]:
                self.visit_cmds(cmd[2])
            else:
                self.add_line("pass")
            self.indent_level -= 1

            if len(cmd) > 3 and cmd[3]:
                self.add_line("else:")
                self.indent_level += 1
                self.visit_cmds(cmd[3])
                self.indent_level -= 1
        elif ctype == 'act_exec':
            val = self.visit_act_exec(cmd)
            self.add_line(val)
        elif ctype == 'act_alert':
            # ('act_alert', msg, observation, devices)
            msg = cmd[1]
            obs = cmd[2]
            devices = cmd[3]
            for dev in devices:
                if obs:
                    self.add_line(f"alerta('{dev}', '{msg}', {obs})")
                else:
                    self.add_line(f"alerta('{dev}', '{msg}')")

    def visit_var(self, var):
        if var[0] == 'num':
            return str(var[1])
        elif var[0] == 'bool':
            return "True" if var[1] else "False"

    def visit_obs(self, obs):
        if obs[0] == 'obs':
            # ('obs', obs_name, op, var)
            val = self.visit_var(obs[3])
            return f"{obs[1]} {obs[2]} {val}"
        elif obs[0] == 'obs_exec':
            # ('obs_exec', act_exec, op, var)
            exec_str = self.visit_act_exec(obs[1])
            val = self.visit_var(obs[3])
            return f"{exec_str} {obs[2]} {val}"
        elif obs[0] == 'obs_and':
            left = self.visit_obs(obs[1])
            right = self.visit_obs(obs[2])
            return f"({left}) and ({right})"

    def visit_act_exec(self, cmd):
        # ('act_exec', action, namedevice)
        return f"{cmd[1]}('{cmd[2]}')"
