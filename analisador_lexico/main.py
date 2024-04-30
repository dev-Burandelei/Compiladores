import sys
from lexer import UCyanLexer  # Certifique-se de que o nome do arquivo com a classe UCyanLexer está correto

def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)

# Create an instance of UCyanLexer with an error function
def error_func(message, line, column):
    print(f"Error at line {line}, column {column}: {message}")

lexer = UCyanLexer(error_func)# Criar uma instância do lexer

# Executar a análise léxica do arquivo "program.txt"
sys.argv = ["lexer.py", "program.txt"]
execfile("lexer.py")

# Ler e analisar o arquivo "program.txt"
input_file = "program.txt"
with open(input_file, 'r') as file:
    text = file.read()
    tokens = lexer.tokenize(text)

# Exibir os tokens
for token in tokens:
    print(token)
