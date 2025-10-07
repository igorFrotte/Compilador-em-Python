from utils.Cor import Cor

class No:
    def __init__(self, tipo, filhos=None, valor=None):
        self.tipo = tipo
        self.filhos = filhos or []
        self.valor = valor

    def printar(self, prefixo="", ultimo=True):
        conector = "└── " if ultimo else "├── "

        tipo_color = Cor.pintar(self.tipo, Cor.AZUL)
        qtd_filhos_texto = f"({len(self.filhos)} filho{'s' if len(self.filhos) != 1 else ''})"
        qtd_filhos = Cor.pintar(qtd_filhos_texto, Cor.CINZA)

        rep = prefixo + conector + f"{tipo_color} {qtd_filhos}"

        if self.valor is not None:
            valor_color = Cor.pintar(self.valor, Cor.VERDE)
            rep += f": {valor_color}"

        rep += "\n"

        prefixo_filho = prefixo + ("    " if ultimo else "│   ")

        for i, filho in enumerate(self.filhos):
            ultimo_filho = i == len(self.filhos) - 1
            rep += filho.printar(prefixo_filho, ultimo_filho)

        return rep

    def __repr__(self):
        return self.printar()
