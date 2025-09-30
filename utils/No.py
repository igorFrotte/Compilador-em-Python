class No:
    def __init__(self, tipo, filhos=None, valor=None):
        self.tipo = tipo
        self.filhos = filhos or []
        self.valor = valor

    def printar(self, nivel=0):
        espaco = "  " * nivel
        rep = f"{espaco}{self.tipo}"
        if self.valor:
            rep += f": {self.valor}"
        rep += "\n"
        for filho in self.filhos:
            rep += filho.printar(nivel + 1)
        return rep

    def __repr__(self):
        return self.printar()
