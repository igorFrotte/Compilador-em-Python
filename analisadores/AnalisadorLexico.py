

class AnalisadorLexico:
    def __init__(self, codigo: str) -> None:
        self.tokens = list()
        self.erros = list()
        self.gerarTokens(codigo)

    def gerarTokens(self, programa: str) -> None:
        print("Gerador de Tokens")