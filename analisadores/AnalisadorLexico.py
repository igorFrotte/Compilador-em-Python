import ply.lex as lex

class AnalisadorLexico:
    # Palavras reservadas
    palavras_reservadas = {
        'program': 'PROGRAM',
        'const': 'CONST',
        'type': 'TYPE',
        'var': 'VAR',
        'function': 'FUNCTION',
        'integer': 'INTEGER',
        'real': 'REAL',
        'array': 'ARRAY',
        'of': 'OF',
        'record': 'RECORD',
        'begin': 'BEGIN',
        'end': 'END',
        'while': 'WHILE',
        'if': 'IF',
        'then': 'THEN',
        'else': 'ELSE',
        'write': 'WRITE',
        'read': 'READ',
    }

    # Lista de tokens
    tokens = [
        'ID',
        'NUMERO',
        'STRING',
        'ATRIBUICAO',
        'DOISPONTOS',
        'PONTOVIRGULA',
        'VIRGULA',
        'PONTO',
        'PARENTESES_ESQ',
        'PARENTESES_DIR',
        'COLCHETE_ESQ',
        'COLCHETE_DIR',
        'OP_LOGICO',
        'OP_MAT',
    ] + list(palavras_reservadas.values())

    # Regras para tokens simples
    t_PONTOVIRGULA = r';'
    t_DOISPONTOS = r':'
    t_ATRIBUICAO = r':='
    t_PONTO = r'\.'
    t_VIRGULA = r','
    t_PARENTESES_ESQ = r'\('
    t_PARENTESES_DIR = r'\)'
    t_COLCHETE_ESQ = r'\['
    t_COLCHETE_DIR = r'\]'

    # Operadores
    t_OP_LOGICO = r'<|>|=|!'
    t_OP_MAT = r'[\+\-\*/]'

    # Tipos especiais
    t_STRING = r'\".*\"'  # string entre aspas
    t_NUMERO = r'\d+(\.\d+)?'

    # Identificadores e palavras reservadas
    def t_ID(self, token):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        token.type = self.palavras_reservadas.get(token.value, 'ID')
        return token

    # Comentários no formato $ ... $
    def t_COMENTARIO(self, t):
        r'\$([^$]*)\$'
        t.lexer.lineno += t.value.count("\n")
        pass

    # Contagem de linhas
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Espaços em branco ignorados
    t_ignore = ' \t\r'

    # Tratamento de erro
    def t_error(self, t):
        self.erros.append((t.value, t.lineno))
        t.lexer.skip(1)

    # Construtor
    def __init__(self, codigo):
        self.lexo = lex.lex(module=self)
        self.erros = list()
        self.tokens = list()
        self.gerarTokens(codigo)
        self.printErros()
        self.printTokens()

    # Função principal
    def gerarTokens(self, codigo):
        self.lexo.input(codigo)
        while True:
            tok = self.lexo.token()
            if not tok:
                break
            self.tokens.append((tok.type, tok.value, tok.lineno))
    
    # Funções auxiliares
    def printTokens(self,):
        for token in self.tokens:
            print(f"{token[0]} {(15-len(token[0]))*' '} linha: {token[2]} {(3-len(str(token[2])))*' '} {token[1]}")
    
    def printErros(self,):
        for token in self.erros:
            print("\033[1;31;40m"+ 
                f"Caracter ilegal '{token[0][0]}' na linha {token[1]}" 
                + "\033[0m")
