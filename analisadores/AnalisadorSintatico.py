from utils.Cor import Cor
from utils.No import No

class AnalisadorSintatico:
    def __init__(self, listaTokens):
        self.tokens = listaTokens  # tuplas (tipo, valor, linha)
        self.pos = 0
        self.arvoreSintatica = self.programa()

    def token_atual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consumir(self, esperado):
        token = self.token_atual()
        if token and token[0] == esperado:
            self.pos += 1
            return No(esperado, valor=token[1])
        else:
            print(Cor.pintar(f"Esperado {esperado}, mas encontrado {token}" , Cor.VERMELHO))
            return No("ERRO", valor=str(token))
            # Tratar erros

    # --- NÃO TERMINAIS ---

    def programa(self):
        # [PROGRAMA] ::= (program) [ID] (;) [CORPO]
        filhos = []
        filhos.append(self.consumir("PROGRAM"))
        filhos.append(self.consumir("ID"))
        filhos.append(self.consumir("PONTOVIRGULA"))
        filhos.append(self.corpo())
        return No("PROGRAMA", filhos)

    def corpo(self):
        # [CORPO] ::= [DECLARACOES] (begin) [LISTA_COM] (end)
        filhos = []
        filhos.append(self.declaracoes())
        filhos.append(self.consumir("BEGIN"))
        #LISTA_COM
        filhos.append(self.consumir("END"))
        return No("CORPO", filhos)

    def declaracoes(self):
        # [DECLARACOES] ::= [DEF_CONST] [DEF_TIPOS] [DEF_VAR] [LISTA_FUNC] | ε
        filhos = []
        # Continuar
        return No("DECLARACOES", filhos)