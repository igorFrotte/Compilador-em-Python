class Cor:
    VERMELHO = "\033[1;31;40m"
    BRANCO   = "\033[0m"
    VERDE    = "\033[92m"
    AZUL = "\033[94m"
    CINZA = "\033[90m"

    @staticmethod
    def pintar(texto, cor):
        return f"{cor}{texto}{Cor.BRANCO}"