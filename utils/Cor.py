class Cor:
    VERMELHO = "\033[1;31;40m"
    BRANCO   = "\033[0m"
    VERDE    = "\033[92m"

    @staticmethod
    def pintar(texto, cor):
        return f"{cor}{texto}{Cor.BRANCO}"