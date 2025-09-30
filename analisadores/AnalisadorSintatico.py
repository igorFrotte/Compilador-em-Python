from utils.Cor import Cor
from utils.No import No
from utils.Token import Token

FIRST = {
    "PROGRAMA": {Token.PROGRAM},
    "CORPO": {Token.CONST.value, Token.TYPE.value, Token.VAR.value, Token.BEGIN.value},
    "DECLARACOES": {Token.CONST.value, Token.TYPE.value, Token.VAR.value, Token.FUNCTION.value},
    "DEF_CONST": {Token.CONST.value},
    "LISTA_CONST": {Token.ID.value},
    "LISTA_CONST'": {Token.ID.value},
    "CONSTANTE": {Token.ID.value},
    "CONST_VALOR": {Token.STRING.value, Token.ID.value, Token.NUMERO.value},
    "DEF_TIPOS": {Token.TYPE.value},
    "LISTA_TIPOS": {Token.ID.value},
    "LISTA_TIPOS'": {Token.PONTO_VIRGULA.value},
    "TIPO": {Token.ID.value},
    "TIPO_DADO": {Token.INTEGER.value, Token.REAL.value, Token.ARRAY.value, Token.RECORD.value, Token.ID.value},
    "DEF_VAR": {Token.VAR.value},
    "LISTA_VAR": {Token.ID.value},
    "LISTA_VAR'": {Token.PONTO_VIRGULA.value},
    "VARIAVEL": {Token.ID.value},
    "LISTA_ID": {Token.ID.value},
    "LISTA_ID'": {Token.VIRGULA.value},
    "LISTA_FUNC": {Token.FUNCTION.value},
    "FUNCAO": {Token.FUNCTION.value},
    "NOME_FUNCAO": {Token.FUNCTION.value},
    "BLOCO_FUNCAO": {Token.VAR, Token.BEGIN.value},
    "BLOCO": {Token.BEGIN.value, Token.ID.value, Token.WHILE.value, Token.IF.value, Token.WRITE.value, Token.READ.value},
    "LISTA_COM": {Token.ID.value, Token.WHILE.value, Token.IF.value, Token.WRITE.value, Token.READ.value},
    "COMANDO": {Token.ID.value, Token.WHILE.value, Token.IF.value, Token.WRITE.value, Token.READ.value},
    "ELSE": {Token.ELSE.value},
    "VALOR": {Token.ID.value, Token.NUMERO.value},
    "LISTA_PARAM": {Token.PARENTESES_ESQ.value},
    "LISTA_NOME": {Token.ID.value, Token.NUMERO.value},
    "LISTA_NOME'": {Token.VIRGULA.value},
    "PARAMETRO": {Token.ID.value, Token.NUMERO.value},
    "EXP_LOGICA": {Token.ID.value, Token.NUMERO.value},
    "EXP_LOGICA'": {Token.OP_LOGICO.value},
    "EXP_MAT": {Token.ID.value, Token.NUMERO.value},
    "EXP_MAT'": {Token.OP_MAT.value},
    "NOME": {Token.ID.value},
    "NOME'": {Token.PONTO.value, Token.PARENTESES_ESQ.value},
}


class AnalisadorSintatico:
    def __init__(self, listaTokens):
        self.tokens = listaTokens  # tuplas (tipo, valor, linha)
        self.pos = 0
        self.arvoreSintatica = self.programa()

    def token_atual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consumir(self, recebido: Token):
        esperado = recebido.value
        token = self.token_atual()
        if token and token[0] == esperado:
            self.pos += 1
            return No(esperado, valor=token[1])
        else:
            print(Cor.pintar(f"Esperado {esperado}, mas encontrado {token}", Cor.VERMELHO))
            return No("ERRO", valor=str(token))

    # --- NÃO TERMINAIS ---

    def programa(self):
        # [PROGRAMA] ::= (program) [ID] (;) [CORPO]
        filhos = []
        filhos.append(self.consumir(Token.PROGRAM))
        filhos.append(self.consumir(Token.ID))
        filhos.append(self.consumir(Token.PONTO_VIRGULA))
        filhos.append(self.corpo())
        return No("PROGRAMA", filhos)

    def corpo(self):
        # [CORPO] ::= [DECLARACOES] (begin) [LISTA_COM] (end)
        #          | (begin) [LISTA_COM] (end)
        filhos = []
        token = self.token_atual()
        if token and token[0] == Token.BEGIN.value:
            filhos.append(self.consumir(Token.BEGIN))
            filhos.append(self.lista_com())
            filhos.append(self.consumir(Token.END))
        else:
            filhos.append(self.declaracoes())
            filhos.append(self.consumir(Token.BEGIN))
            filhos.append(self.lista_com())
            filhos.append(self.consumir(Token.END))
        return No("CORPO", filhos)

    def declaracoes(self):
        # [DECLARACOES] ::= [DEF_CONST] [DEF_TIPOS] [DEF_VAR] [LISTA_FUNC] | ε
        filhos = []
        if(self.token_atual()[0] in FIRST["DEF_CONST"]):
            filhos.append(self.def_const())
            filhos.append(self.def_tipos())
            filhos.append(self.def_var())
            filhos.append(self.lista_func())
        return No("DECLARACOES", filhos)

    def def_const(self):
        # [DEF_CONST] ::= (const) [LISTA_CONST] | ε
        filhos = []
        token = self.token_atual()
        if token and token[0] == Token.CONST.value:
            filhos.append(self.consumir(Token.CONST))
            filhos.append(self.lista_const())
        return No("DEF_CONST", filhos)

    def lista_const(self):
        # [LISTA_CONST] ::= [CONSTANTE] [LISTA_CONST’]
        filhos = []
        filhos.append(self.constante())
        filhos.append(self.lista_const_())
        return No("LISTA_CONST", filhos)

    def lista_const_(self):
        # [LISTA_CONST’] ::= [LISTA_CONST] | ε
        filhos = []
        if(self.token_atual()[0] in FIRST["LISTA_CONST"]):
            filhos.append(self.lista_const())
        return No("LISTA_CONST'", filhos)

    def constante(self):
        # [CONSTANTE] ::= [ID] (:=) [CONST_VALOR] (;)
        filhos = []
        filhos.append(self.consumir(Token.ID))
        filhos.append(self.consumir(Token.ATRIBUICAO))
        filhos.append(self.const_valor())
        filhos.append(self.consumir(Token.PONTO_VIRGULA))
        return No("CONSTANTE", filhos)

    def const_valor(self):
        # [CONST_VALOR] ::= (“) sequência alfanumérica (“) | [EXP_MAT]
        token = self.token_atual()
        if token and token[0] == Token.STRING.value:
            return self.consumir(Token.STRING)
        else:
            return self.exp_mat()

    def def_tipos(self):
        # [DEF_TIPOS] ::= (type) [LISTA_TIPOS] | ε
        filhos = []
        token = self.token_atual()
        if token and token[0] == Token.TYPE.value:
            filhos.append(self.consumir(Token.TYPE))
            filhos.append(self.lista_tipos())
        return No("DEF_TIPOS", filhos)

    def lista_tipos(self):
        # [LISTA_TIPOS] ::= [TIPO] [LISTA_TIPOS’]
        filhos = []
        filhos.append(self.tipo())
        filhos.append(self.lista_tipos_())
        return No("LISTA_TIPOS", filhos)

    def lista_tipos_(self):
        # [LISTA_TIPOS’] ::= (;) [LISTA_TIPOS] | ε
        filhos = []
        token = self.token_atual()
        if token and token[0] == Token.PONTO_VIRGULA.value:
            filhos.append(self.consumir(Token.PONTO_VIRGULA))
            filhos.append(self.lista_tipos())
        return No("LISTA_TIPOS'", filhos)

    def tipo(self):
        # [TIPO] ::= [ID] (:=) [TIPO_DADO]
        filhos = []
        filhos.append(self.consumir(Token.ID))
        filhos.append(self.consumir(Token.ATRIBUICAO))
        filhos.append(self.tipo_dado())
        return No("TIPO", filhos)

    def tipo_dado(self):
        # [TIPO_DADO] ::= (integer) | (real) | (array) ([) [NUMERO] (]) (of) [TIPO_DADO] | (record) [LISTA_VAR] (end) | [ID]
        token = self.token_atual()
        filhos = []
        if token and token[0] == Token.INTEGER.value:
            filhos.append(self.consumir(Token.INTEGER))
        elif token and token[0] == Token.REAL.value:
            filhos.append(self.consumir(Token.REAL))
        elif token and token[0] == Token.ARRAY.value:
            filhos.append(self.consumir(Token.ARRAY))
            filhos.append(self.consumir(Token.COLCHETE_ESQ))
            filhos.append(self.consumir(Token.NUMERO))
            filhos.append(self.consumir(Token.COLCHETE_DIR))
            filhos.append(self.consumir(Token.OF))
            filhos.append(self.tipo_dado())
        elif token and token[0] == Token.RECORD.value:
            filhos.append(self.consumir(Token.RECORD))
            filhos.append(self.lista_var())
            filhos.append(self.consumir(Token.END))
        elif token and token[0] == Token.ID.value:
            filhos.append(self.consumir(Token.ID))
        else:
            print(Cor.pintar(f"Tipo de dado esperado, mas encontrado {token}", Cor.VERMELHO))
            filhos.append(No("ERRO", valor=str(token)))
        return No("TIPO_DADO", filhos)

    def def_var(self):
        # [DEF_VAR] ::= (var) [LISTA_VAR] | ε
        filhos = []
        token = self.token_atual()
        if token and token[0] == Token.VAR.value:
            filhos.append(self.consumir(Token.VAR))
            filhos.append(self.lista_var())
        return No("DEF_VAR", filhos)

    def lista_var(self):
        # [LISTA_VAR] ::= [VARIAVEL] [LISTA_VAR’] ----------------------  PRECISA SER ε TBM
        filhos = []
        if(self.token_atual()[0] in FIRST["VARIAVEL"]):
            filhos.append(self.variavel())
            filhos.append(self.lista_var_())
        return No("LISTA_VAR", filhos)

    def lista_var_(self):
        # [LISTA_VAR’] ::= (;) [LISTA_VAR] | ε
        filhos = []
        token = self.token_atual()
        if token and token[0] == Token.PONTO_VIRGULA.value:
            filhos.append(self.consumir(Token.PONTO_VIRGULA))
            filhos.append(self.lista_var())
        return No("LISTA_VAR'", filhos)

    def variavel(self):
        # [VARIAVEL] ::= [LISTA_ID] (:) [TIPO_DADO]
        filhos = []
        filhos.append(self.lista_id())
        filhos.append(self.consumir(Token.DOIS_PONTOS))
        filhos.append(self.tipo_dado())
        return No("VARIAVEL", filhos)

    def lista_id(self):
        # [LISTA_ID] ::= [ID] [LISTA_ID’]
        filhos = []
        filhos.append(self.consumir(Token.ID))
        filhos.append(self.lista_id_())
        return No("LISTA_ID", filhos)

    def lista_id_(self):
        # [LISTA_ID’] ::= (,) [LISTA_ID] | ε
        filhos = []
        token = self.token_atual()
        if token and token[0] == Token.VIRGULA.value:
            filhos.append(self.consumir(Token.VIRGULA))
            filhos.append(self.lista_id())
        return No("LISTA_ID'", filhos)

    def lista_func(self):
        # [LISTA_FUNC] ::= [FUNCAO] [LISTA_FUNC] | ε
        filhos = []
        if(self.token_atual()[0] in FIRST["FUNCAO"]):
            filhos.append(self.funcao())
            filhos.append(self.lista_func())
        return No("LISTA_FUNC", filhos)

    def funcao(self):
        # [FUNCAO] ::= [NOME_FUNCAO] [BLOCO_FUNCAO]
        filhos = []
        filhos.append(self.nome_funcao())
        filhos.append(self.bloco_funcao())
        return No("FUNCAO", filhos)

    def nome_funcao(self):
        # [NOME_FUNCAO] ::= (function) [ID] (() [LIST_VAR] ()) (:) [TIPO_DADO]
        filhos = []
        filhos.append(self.consumir(Token.FUNCTION))
        filhos.append(self.consumir(Token.ID))
        filhos.append(self.consumir(Token.PARENTESES_ESQ))
        filhos.append(self.lista_var())
        filhos.append(self.consumir(Token.PARENTESES_DIR))
        filhos.append(self.consumir(Token.DOIS_PONTOS))
        filhos.append(self.tipo_dado())
        return No("NOME_FUNCAO", filhos)

    def bloco_funcao(self):
        # [BLOCO_FUNCAO] ::= [DEF_VAR] [BLOCO]
        filhos = []
        filhos.append(self.def_var())
        filhos.append(self.bloco())
        return No("BLOCO_FUNCAO", filhos)

    def bloco(self):
        # [BLOCO] ::= (begin) [LISTA_COM] (end) | [COMANDO]
        token = self.token_atual()
        if token and token[0] == Token.BEGIN.value:
            filhos = []
            filhos.append(self.consumir(Token.BEGIN))
            filhos.append(self.lista_com())
            filhos.append(self.consumir(Token.END))
            return No("BLOCO", filhos)
        else:
            return self.comando()

    def lista_com(self):
        # [LISTA_COM] ::= [COMANDO] (;) [LISTA_COM] | ε
        filhos = []
        if(self.token_atual()[0] in FIRST["COMANDO"]):
            filhos.append(self.comando())
            filhos.append(self.consumir(Token.PONTO_VIRGULA))
            filhos.append(self.lista_com())
        return No("LISTA_COM", filhos)

    def comando(self):
        # [COMANDO] ::= [NOME] (:=) [VALOR]
        #            | (while) [EXP_LOGICA] [BLOCO]
        #            | (if) [EXP_LOGICA] (then) [BLOCO] [ELSE]
        #            | (write) [CONST_VALOR]
        #            | (read) [NOME]
        token = self.token_atual()
        filhos = []
        if not token:
            return No("COMANDO", filhos)

        if token[0] == Token.ID.value:
            filhos.append(self.nome())
            filhos.append(self.consumir(Token.ATRIBUICAO))
            filhos.append(self.valor())
        elif token[0] == Token.WHILE.value:
            filhos.append(self.consumir(Token.WHILE))
            filhos.append(self.exp_logica())
            filhos.append(self.bloco())
        elif token[0] == Token.IF.value:
            filhos.append(self.consumir(Token.IF))
            filhos.append(self.exp_logica())
            filhos.append(self.consumir(Token.THEN))
            filhos.append(self.bloco())
            filhos.append(self.else_())
        elif token[0] == Token.WRITE.value:
            filhos.append(self.consumir(Token.WRITE))
            filhos.append(self.const_valor())
        elif token[0] == Token.READ.value:
            filhos.append(self.consumir(Token.READ))
            filhos.append(self.nome())
        else:
            print(Cor.pintar(f"Comando esperado, mas encontrado {token}", Cor.VERMELHO))
            filhos.append(No("ERRO", valor=str(token)))
        return No("COMANDO", filhos)

    def else_(self):
        # [ELSE] ::= (else) [BLOCO] | ε
        filhos = []
        token = self.token_atual()
        if token and token[0] == Token.ELSE.value:
            filhos.append(self.consumir(Token.ELSE))
            filhos.append(self.bloco())
        return No("ELSE", filhos)

    def valor(self):
        # [VALOR] ::= [EXP_MAT] | [ID] [LISTA_PARAM]
        filhos = []
        token = self.token_atual()
        if token and token[0] == Token.ID.value:
            next_token = self.tokens[self.pos + 1]
            if next_token and next_token[0] in FIRST["LISTA_PARAM"]:
                filhos.append(self.consumir(Token.ID))
                filhos.append(self.lista_param())
                return No("VALOR", filhos)
            else:
                filhos.append(self.exp_mat())
                return No("VALOR", filhos)
        if token and token[0] == Token.NUMERO.value:   
            filhos.append(self.exp_mat())
            return No("VALOR", filhos)
        

    def lista_param(self):
        # [LISTA_PARAM] ::= (() [LISTA_NOME] ()) | ε
        filhos = []
        token = self.token_atual()
        if token and token[0] == Token.PARENTESES_ESQ.value:
            filhos.append(self.consumir(Token.PARENTESES_ESQ))
            filhos.append(self.lista_nome())
            filhos.append(self.consumir(Token.PARENTESES_DIR))
        return No("LISTA_PARAM", filhos)

    def lista_nome(self):
        # [LISTA_NOME] ::= [PARAMETRO] [LISTA_NOME’]
        filhos = []
        token = self.token_atual()
        if token and token[0] in [Token.ID.value, Token.NUMERO.value]:
            filhos.append(self.parametro())
            filhos.append(self.lista_nome_())
        return No("LISTA_NOME", filhos)

    def lista_nome_(self):
        # [LISTA_NOME’] ::= (,) [LISTA_NOME] | ε
        filhos = []
        token = self.token_atual()
        if token and token[0] == Token.VIRGULA.value:
            filhos.append(self.consumir(Token.VIRGULA))
            filhos.append(self.lista_nome())
        return No("LISTA_NOME'", filhos)

    def parametro(self):
        # [PARAMETRO] ::= [NOME] | [NUMERO]
        token = self.token_atual()
        if token[0] == Token.ID.value:
            return self.nome()
        else:
            return self.consumir(Token.NUMERO)

    def exp_logica(self):
        # [EXP_LOGICA] ::= [EXP_MAT] [EXP_LOGICA’]
        filhos = []
        filhos.append(self.exp_mat())
        filhos.append(self.exp_logica_())
        return No("EXP_LOGICA", filhos)

    def exp_logica_(self):
        # [EXP_LOGICA’] ::= [OP_LOGICO] [EXP_LOGICA] | ε
        filhos = []
        token = self.token_atual()
        if token and token[0] == Token.OP_LOGICO.value:
            filhos.append(self.consumir(Token.OP_LOGICO))
            filhos.append(self.exp_logica())
        return No("EXP_LOGICA'", filhos)

    def exp_mat(self):
        # [EXP_MAT] ::= [PARAMETRO] [EXP_MAT’]
        filhos = []
        filhos.append(self.parametro())
        filhos.append(self.exp_mat_())
        return No("EXP_MAT", filhos)

    def exp_mat_(self):
        # [EXP_MAT’] ::= [OP_MAT] [EXP_MAT] | ε
        filhos = []
        token = self.token_atual()
        if token and token[0] == Token.OP_MAT.value:
            filhos.append(self.consumir(Token.OP_MAT))
            filhos.append(self.exp_mat())
        return No("EXP_MAT'", filhos)

    def nome(self):
        # [NOME] ::= [ID] [NOME’]
        filhos = []
        filhos.append(self.consumir(Token.ID))
        filhos.append(self.nome_())
        return No("NOME", filhos)

    def nome_(self):
        # [NOME’] ::= (.) [NOME] | ([) [PARAMETRO] (]) | ε
        filhos = []
        token = self.token_atual()
        if token and token[0] == Token.PONTO.value:
            filhos.append(self.consumir(Token.PONTO))
            filhos.append(self.nome())
        elif token and token[0] == Token.COLCHETE_ESQ.value:
            filhos.append(self.consumir(Token.COLCHETE_ESQ))
            filhos.append(self.parametro())
            filhos.append(self.consumir(Token.COLCHETE_DIR))
        return No("NOME'", filhos)

