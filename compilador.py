from analisadores.AnalisadorLexico import AnalisadorLexico
from analisadores.AnalisadorSintatico import AnalisadorSintatico
from sys import argv

file = open(argv[1], 'r') # python3 compilador.py arquivo.txt
code = file.read()

Lexo = AnalisadorLexico(code)
Sintatico = AnalisadorSintatico(Lexo.tokens)



