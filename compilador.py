from analisadores.AnalisadorLexico import AnalisadorLexico
from analisadores.AnalisadorSintatico import AnalisadorSintatico
from sys import argv

file = open(argv[1], 'r') # python3 compilador.py arquivo.txt
code = file.read()

Lexo = AnalisadorLexico(code)
Lexo.printErros()
#Lexo.printTokens()

if not Lexo.erros:
    Sintatico = AnalisadorSintatico(Lexo.tokens)
    print(Sintatico.arvoreSintatica)






