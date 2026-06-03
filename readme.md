# Trabalho Final INF1022 - 2026.1

Repositório do trabalho final da disciplina INF1022. O objetivo aqui é construir um analisador sintático/transpilador para a linguagem `ObsAct`, conforme o enunciado.

Estamos usando **Python** e a biblioteca **PLY** (Python Lex-Yacc) para criar o Analisador Léxico e o Analisador Sintático (usando parser LALR(1)).

## Como testar e rodar

1. Primeiro, cria e ativa o ambiente virtual (pra não sujar o Python global):
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

2. Instala o PLY (a única dependência real):
   ```bash
   pip install -r requirements.txt
   ```

3. Pra compilar um arquivo escrito em ObsAct:
   ```bash
   python src/main.py testes/meu_teste.txt
   ```
