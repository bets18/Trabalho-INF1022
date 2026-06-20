class ObsActTranspiler:
    def transpile(self, ast):
        # Cabeçalho do C e funções base da linguagem
        c_code = "#include <stdio.h>\n\n"
        c_code += "int ligar(char* name) { printf(\"%s ligado!\\n\", name); return 1; }\n"
        c_code += "int desligar(char* name) { printf(\"%s desligado!\\n\", name); return 0; }\n"
        c_code += "int verificar(char* name) { printf(\"%s estado verificado.\\n\", name); return 1; }\n"
        c_code += "void alerta_msg(char* name, char* msg) { printf(\"%s recebeu o alerta: \\n%s\\n\", name, msg); }\n"
        c_code += "void alerta_var(char* name, char* msg, int var) { printf(\"%s recebeu o alerta: \\n%s %d\\n\", name, msg, var); }\n"
        
        # FEATURE EXTRA: Agendar e Fechar
        c_code += "int agendar(char* name, char* hora) { printf(\"Alarme agendado no %s para as %s\\n\", name, hora); return 1; }\n"
        c_code += "int fechar(char* name) { printf(\"%s fechado!\\n\", name); return 1; }\n\n"
        
        # Função principal
        c_code += "int main() {\n"
        
        # Percorre a AST para preencher o corpo do main
        c_code += self.walk(ast, 1)
        
        c_code += "    return 0;\n"
        c_code += "}\n"
        return c_code

    def walk(self, node, indent):
        if not node:
            return ""
        
        # Configuração de indentação (4 espaços por nível)
        ind = "    " * indent
        
        # Se for uma lista de nós, processa recursivamente todos eles
        if isinstance(node, list):
            result = ""
            for n in node:
                result += self.walk(n, indent)
            return result

        # Se for uma tupla, processa o respectivo nó da AST
        if isinstance(node, tuple):
            node_type = node[0]

            if node_type == 'program':
                devices = node[1]
                cmds = node[2]
                code = ""
                # Processa os devices para encontrar variáveis declaradas
                for d in devices:
                    if len(d) == 3:  # Ex: ('device', 'Termometro', 'temperatura')
                        var_name = d[2]
                        # Declara a variável em C
                        code += f"{ind}int {var_name} = 0;\n"
                
                if code:  # Adiciona linha extra se houve declaração de variáveis
                    code += "\n"
                    
                # Processa todos os comandos e anexa o código retornado
                code += self.walk(cmds, indent)
                return code

            elif node_type == 'attrib':
                var_name = node[1]
                value = self.walk(node[2], 0)
                return f"{ind}{var_name} = {value};\n"

            elif node_type == 'if':
                cond = self.walk(node[1], 0)
                cmds_if = self.walk(node[2], indent + 1)
                return f"{ind}if ({cond}) {{\n{cmds_if}{ind}}}\n"

            elif node_type == 'if_else':
                cond = self.walk(node[1], 0)
                cmds_if = self.walk(node[2], indent + 1)
                cmds_else = self.walk(node[3], indent + 1)
                return f"{ind}if ({cond}) {{\n{cmds_if}{ind}}} else {{\n{cmds_else}{ind}}}\n"

            elif node_type == 'condition':
                var1 = node[1]
                op = node[2]
                var2 = self.walk(node[3], 0)
                return f"{var1} {op} {var2}"

            elif node_type == 'condition_and':
                var1 = node[1]
                op = node[2]
                var2 = self.walk(node[3], 0)
                obs_next = self.walk(node[4], 0)
                return f"{var1} {op} {var2} && {obs_next}"

            elif node_type == 'num':
                # Valores numéricos (folha da árvore)
                return str(node[1])

            elif node_type == 'bool':
                # Booleano mapeado para C: True=1, False=0
                return "1" if node[1] else "0"

            elif node_type == 'act':
                action = node[1]
                device = node[2]
                return f"{ind}{action}(\"{device}\");\n"

            elif node_type == 'alert':
                msg = node[1]
                device = node[2]
                return f"{ind}alerta_msg(\"{device}\", \"{msg}\");\n"

            elif node_type == 'alert_var':
                msg = node[1]
                var = node[2]
                device = node[3]
                return f"{ind}alerta_var(\"{device}\", \"{msg}\", {var});\n"

            elif node_type == 'alert_broadcast':
                msg = node[1]
                devices_list = node[2]
                code = ""
                # Faz o loop no gerador em Python para criar múltiplos disparos de mensagem em C
                for device in devices_list:
                    code += f"{ind}alerta_msg(\"{device}\", \"{msg}\");\n"
                return code

            # FEATURE EXTRA: Agendar
            elif node_type == 'agendar':
                device = node[1]
                hora = node[2]
                return f"{ind}agendar(\"{device}\", \"{hora}\");\n"

        return ""
