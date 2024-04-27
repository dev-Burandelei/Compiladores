import sys

def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)

# execute the file
sys.argv = ["lexer.py", "program.txt"]
execfile("lexer.py")
sys.argv = ["lexer.py", "tokens.txt"]
execfile("lexer.py")