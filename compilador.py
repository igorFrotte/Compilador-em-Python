import sys
from analisadores.AnalisadorLexico import AnalisadorLexico
from analisadores.AnalisadorSintatico import AnalisadorSintatico 

def main():
    if len(sys.argv) < 2:
        print("Erro: Nenhum arquivo foi informado.")
        print("Como Usar: python3 compilador.py <arquivo.txt> [showTokens | showTree | showAll]")
        sys.exit(1)

    arquivo = sys.argv[1]
    try:
        with open(arquivo, 'r') as file:
            code = file.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo}' não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        sys.exit(1)

    Lexo = AnalisadorLexico(code)
    Lexo.printErros()

    if Lexo.erros:
        sys.exit(1)

    Sintatico = AnalisadorSintatico(Lexo.tokens)

    if len(sys.argv) > 2:
        opcao = sys.argv[2].lower()
    else:
        opcao = None

    if opcao == "showtokens":
        Lexo.printTokens()
    elif opcao == "showtree":
        print(Sintatico.arvoreSintatica)
    elif opcao == "showall":
        Lexo.printTokens()
        print(Sintatico.arvoreSintatica)
    elif opcao is None:
        print("")
    else:
        print(f"Opção '{opcao}' não reconhecida.")
        print("Opções válidas: showTokens | showTree | showAll")

if __name__ == "__main__":
    main()





