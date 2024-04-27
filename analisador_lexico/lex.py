import sys
sys.path.insert(0, 'sly.zip')
from sly import Lexer

class uCyanLexer(Lexer):
  """A lexer for the uCyan language."""

  # Reserved keywords
  keywords = {
    'print': "PCPrint",
    'if': "PCIf",
    '=': "PCAssingment",
    'while': "PCWhile",
    'break': "PCBreal",
    'continue': "PCContinue",
    'let': "PCLet",
    'var' : "PCVar",
    'int' : "PCIntereger",
    'float' : "PCFloat",
    'char' : "PCChar",
    'true': "OpLogTrue",
    'false': "OpLogFalse"
  }

  # All the tokens recognized by the lexer
  tokens = tuple(keywords.values()) + (
    # Identifiers
    "Var",
    # Constants
    "NumInt",
    "NumReal",
    "Cadeia",
    # Operators 
    "OpAritSoma",
    "OpAritSub",
    "OpAritMult",
    "OpAritDiv",
    "OpRelMenor",
    "OpRelMenorIgual",
    "OpRelMaior",
    "OpRelMaiorIgual",
    "OpRelIgualdade",
    "OpRelDif",
    "OpLogE",
    "OpLogOu",
    # Unitary Operators
    "OpUnarySoma",
    "OpUnarySub",
    "OPUnaryDif"
    # Delimeters
    "Delim",
    "AbrePar",
    "FechaPar",
  )

  # String containing ignored characters (between tokens)
  ignore = ' \t'

  # Other ignored patterns
  ignore_newline = r'\n+'
  ignore_comment = r'\%.*\r?\n'

  # Regular expression rules for tokens
  Var = r'[a-zA-Z][a-zA-Z0-9]*'
  NumReal = r'\d+\.\d+'
  NumInt = r'\d+'
  Cadeia = r'\'([^\\\n]|(\\.))*?\''
  OpAritSoma = r'\+'
  OpAritSub = r'-'
  OpAritMult = r'\*'
  OpAritDiv = r'\/'
  OpRelIgual = r'='
  OpRelDif = r'<>'
  OpRelMenorIgual = r'<='
  OpRelMenor = r'<'
  OpRelMaiorIgual = r'>='
  OpRelMaior = r'>'
  Delim = r':'
  AbrePar = r'\('
  FechaPar = r'\)'

  # Special cases
  def Var(self, t):
    t.type = self.keywords.get(t.value, "Var")
    return t

  # Define a rule so we can track line numbers
  def ignore_newline(self, t):
    self.lineno += len(t.value)
 
  def ignore_comment(self, t):
    self.lineno += t.value.count("\n")

  def find_column(self, token):
    """Find the column of the token in its line."""
    last_cr = self.text.rfind('\n', 0, token.index)
    return token.index - last_cr

  # Error handling rule
  def error(self, t):
    print("Illegal character %s at position (%d,%d)" % \
          (repr(t.value[0]), t.lineno, self.find_column(t)))
    self.index += 1
    
def main(args):
  if len(args) > 0:
    lex = uCyanLexer()
    with open(args[0], 'r') as f:
      for t in lex.tokenize(f.read()):
        print("<%s,%s>" % (t.type, t.value))

if __name__ == "__main__" :
  main(sys.argv[1:])