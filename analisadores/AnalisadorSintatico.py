

class AnalisadorSintatico:
    def __init__(self, listaTokens) -> None:
        self.percorrerTokens(listaTokens)
        self.arvoreSintatica = list()

    def percorrerTokens(self, listaTokens : list) -> None:
        print("Percorrer Tokens")