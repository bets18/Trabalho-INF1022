# Compilador ObsAct 🏠

Este projeto é um analisador sintático e transpilador desenvolvido em Python para a linguagem **ObsAct** (linguagem de automação de dispositivos inteligentes), como parte do Trabalho Final da disciplina de Compiladores (INF1022 - 2026.1).

O compilador lê um código escrito na sintaxe do ObsAct e gera o código equivalente em **C**, mantendo as inicializações, condições, lógicas e chamadas de ação.

## 🚀 Funcionalidades

- **Mapeamento de Dispositivos e Variáveis:** O código reconhece declarações dinâmicas e inicializa variáveis com `0` por padrão.
- **Estruturas Condicionais e Lógicas:** Suporta blocos `se / entao / senao` aninhados e cadeias de condições com `&&`.
- **Comandos de Ação Padrão:** Implementa `ligar`, `desligar`, `verificar` e envio de `alerta`.
- **(Extra) Ação de Agendamento:** Permite agendar execuções em horas específicas (ex: `agendar Celular 07:00`).
- **(Extra) Ação Física:** Comando `fechar` para dispositivos como portas e cortinas.
- **(Extra) Envio de Alertas em Lote:** Permite envio de `alerta` em broadcast usando `para todos: ...`.

## 🛠️ Como Executar

### Pré-requisitos
- **Python 3.x**
- Biblioteca **SLY**: `pip install sly`
- Compilador **GCC** (para compilar o arquivo C resultante)

### Passos

1. Edite o arquivo `teste.obsact` com os comandos desejados na linguagem ObsAct.
2. No terminal, execute o compilador:
   ```bash
   python main.py
   ```
3. O transpilador lerá o arquivo `.obsact` e gerará automaticamente um arquivo `saida.c` com o código traduzido.
4. Compile o código C gerado e execute-o:
   ```bash
   gcc saida.c -o saida
   .\saida.exe  # No Windows
   ./saida      # No Linux / Mac
   ```

## 🧑‍💻 Autores
- Victor Hugo Moreira Brito (2421278)
- Rafaela Bessa Garcia de Oliveira (2420043)
