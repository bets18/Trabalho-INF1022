class ObsActTranspiler:
    def transpile(self, ast):
        # Aqui a gente começa a criar o código em C que vai ser gerado.
        # Primeiro, incluímos as bibliotecas e criamos as funções base que simulam nossos dispositivos.
        c_code = "#include <stdio.h>\n\n"
        
        # Funções "mockadas" (de mentirinha) em C só para imprimir no terminal e a gente ver que funcionou.
        c_code += "int ligar(char* name) { printf(\"%s ligado!\\n\", name); return 1; }\n"
        c_code += "int desligar(char* name) { printf(\"%s desligado!\\n\", name); return 0; }\n"
        c_code += "int verificar(char* name) { printf(\"%s estado verificado.\\n\", name); return 1; }\n"
        c_code += "void alerta_msg(char* name, char* msg) { printf(\"%s recebeu o alerta: \\n%s\\n\", name, msg); }\n"
        c_code += "void alerta_var(char* name, char* msg, int var) { printf(\"%s recebeu o alerta: \\n%s %d\\n\", name, msg, var); }\n"
        
        # FEATURE EXTRA: Funções adicionais que criamos para nossa linguagem, como agendar e fechar coisas.
        c_code += "int agendar(char* name, char* hora) { printf(\"Alarme agendado no %s para as %s\\n\", name, hora); return 1; }\n"
        c_code += "int fechar(char* name) { printf(\"%s fechado!\\n\", name); return 1; }\n\n"
        
        # Aqui começa a função principal do programa em C (o int main)
        c_code += "int main() {\n"
        
        # O método self.walk vai percorrer a nossa Árvore Sintática (AST) gerada pelo parser
        # Ele vai traduzindo cada pedaço da árvore e preenchendo o corpo do main em C
        c_code += self.walk(ast, 1)
        
        # Finaliza o main com return 0, que é padrão do C para indicar que deu tudo certo
        c_code += "    return 0;\n"
        c_code += "}\n"
        
        # Devolve o código C inteirinho pronto pra ser salvo num arquivo (saida.c)
        return c_code

    def walk(self, node, indent):
        # Se o nó for vazio, não faz nada e devolve string vazia
        if not node:
            return ""
        
        # Ajusta os espaços da indentação pra o código C final ficar bonitinho e legível (4 espaços por nível)
        ind = "    " * indent
        
        # Se tivermos uma lista de comandos (um bloco de código), a gente chama o walk recursivamente em cada um deles
        if isinstance(node, list):
            result = ""
            for n in node:
                result += self.walk(n, indent)
            return result

        # Se for uma tupla, significa que chegamos num nó específico da nossa AST
        if isinstance(node, tuple):
            node_type = node[0] # Pega o tipo do nó (ex: 'if', 'attrib', 'act', etc)

            if node_type == 'program':
                # 'program' é a raiz de tudo. Tem a parte dos dispositivos (devices) e dos comandos do sistema (cmds)
                devices = node[1]
                cmds = node[2]
                code = ""
                
               
                for d in devices:
                    if len(d) == 3:  # Ex de d: ('device', 'Termometro', 'temperatura')
                        var_name = d[2]
                        # Cria a variável em C, algo tipo: int temperatura = 0;
                        code += f"{ind}int {var_name} = 0;\n"
                
                if code:  # Se criamos variáveis, damos uma quebra de linha só pra separar dos comandos
                    code += "\n"
                    
                # Depois de declarar as variáveis, manda o walk processar todos os comandos lógicos de fato
                code += self.walk(cmds, indent)
                return code

            elif node_type == 'attrib':
                # Nó de atribuição, tipo 'temperatura = 20'.
                # node[1] é o nome da variável, e processamos o node[2] pra pegar o valor final.
                var_name = node[1]
                value = self.walk(node[2], 0)
                return f"{ind}{var_name} = {value};\n"

            elif node_type == 'if':
                # Estrutura 'se'. Transforma a condição e o bloco de comandos de dentro dele pra C.
                cond = self.walk(node[1], 0)
                cmds_if = self.walk(node[2], indent + 1) # indent+1 pra dar o "tab" dentro do if
                return f"{ind}if ({cond}) {{\n{cmds_if}{ind}}}\n"

            elif node_type == 'if_else':
                # Estrutura 'se / senao'. Mesma lógica do if, mas processamos também o bloco do else (node[3]).
                cond = self.walk(node[1], 0)
                cmds_if = self.walk(node[2], indent + 1)
                cmds_else = self.walk(node[3], indent + 1)
                return f"{ind}if ({cond}) {{\n{cmds_if}{ind}}} else {{\n{cmds_else}{ind}}}\n"

            elif node_type == 'condition':
                # Condição simples (ex: temperatura > 30). Retornamos no formato pro C.
                var1 = node[1]
                op = node[2]
                var2 = self.walk(node[3], 0)
                return f"{var1} {op} {var2}"

            elif node_type == 'condition_and':
                # Condição com 'E' lógico (and). Junta duas condições usando o operador '&&' do C.
                var1 = node[1]
                op = node[2]
                var2 = self.walk(node[3], 0)
                obs_next = self.walk(node[4], 0)
                return f"{var1} {op} {var2} && {obs_next}"

            elif node_type == 'num':
                # Pega só o valor do número (é a ponta final, a folha da nossa árvore)
                return str(node[1])

            elif node_type == 'bool':
                # O C não tem booleano nativo padrão ativado por default na mesma forma, então convertemos pra 1 (True) e 0 (False)
                return "1" if node[1] else "0"

            elif node_type == 'act':
                # Ação simples num dispositivo, tipo 'ligar "Luz"'.
                action = node[1]
                device = node[2]
                return f"{ind}{action}(\"{device}\");\n"

            elif node_type == 'alert':
                # Envia um alerta simples, passando pra função alerta_msg do C.
                msg = node[1]
                device = node[2]
                return f"{ind}alerta_msg(\"{device}\", \"{msg}\");\n"

            elif node_type == 'alert_var':
                # Alerta avançado que manda junto o valor da variável lida.
                msg = node[1]
                var = node[2]
                device = node[3]
                return f"{ind}alerta_var(\"{device}\", \"{msg}\", {var});\n"

            elif node_type == 'alert_broadcast':
                # Estrutura pra quando queremos disparar o alerta pra VÁRIOS dispositivos ao mesmo tempo.
                msg = node[1]
                devices_list = node[2]
                code = ""
                # Fazemos o loop e criamos várias chamadas de função 'alerta_msg' em C (uma pra cada device na lista).
                for device in devices_list:
                    code += f"{ind}alerta_msg(\"{device}\", \"{msg}\");\n"
                return code

            # FEATURE EXTRA: Agendar
            elif node_type == 'agendar':
                # Chama a nossa função em C simulando o agendamento de um horário no device
                device = node[1]
                hora = node[2]
                return f"{ind}agendar(\"{device}\", \"{hora}\");\n"

        # Se não cair em nada, retorna vazio. Isso evita que o transpiler quebre no meio
        return ""
