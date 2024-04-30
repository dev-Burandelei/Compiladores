class UCyanLexer(Lexer):
    """A lexer for the uCyan language."""

    def __init__(self, error_func):
        """Create a new Lexer.
        An error function. Will be called with an error
        message, line and column as arguments, in case of
        an error during lexing.
        """
        self.error_func = error_func
        
    # Reserved keywords
    keywords = {
        'let': "LET",
        'var': "VAR",
        'print': "PRINT",
        'break': "BREAK",
        'continue': "CONTINUE",
        'if': "IF",
        'else': "ELSE",
        'while': "WHILE",
        'true': "TRUE",
        'false': "FALSE",
    }

    # All the tokens recognized by the lexer
    tokens = tuple(keywords.values()) + (
       # Identifiers
        "ID",

        # Constants
        "FLOAT_CONST",
        "INT_CONST",
        "CHAR_CONST",

        # Operators
        "PLUS",
        "MINUS",
        "TIMES",
        "DIVIDE",
        "LE",
        "LT",
        "GE",
        "GT",
        "EQ",
        "NE",
        "AND",
        "OR",
        "NOT",

        # Assignment
        "EQUALS",

        # Delimeters
        "SEMI",
        "LPAREN",
        "RPAREN",
        "LBRACE",
        "RBRACE",

        "UNCOMMENT",
        # Unitary Operators
        "OpUnarySoma",
        "OpUnarySub",
        "OPUnaryDif",
        "error_char",
        "error_comment",
    )

    # String containing ignored characters (between tokens)
    ignore = " \t"

    # Other ignored patterns
    ignore_newline = r'\n+'
    #ignore_uncomment = r'\/\*.*?\*\/'
    #ignore_multiline = r'\/\*(.|\n)*?\*\/'
    ignore_comment = r'\/\*(.|\n)*?\*\/|\/\/.*'
    error_comment = r'\/\*(.|\n)*'


    # Regular expression rules for tokens
    CHAR_CONST = r'\'([^\\\n]|(\\.))*?\''
    ID = r'[a-zA-Z_][0-9a-zA-Z_]*'
    FLOAT_CONST = r'\d+\.\d+'
    INT_CONST = r'\d+'
    

    error_char = r'\'.*'
    # Binary operators
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'\/'
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    EQ = r'=='
    NE = r'\!\='
    OR = '\|\|'
    AND = r'\&\&'
    NOT = r'\!'

    EQUALS = r'='
    # Delimitadores
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACE = r'\{|\['
    RBRACE = r'\}|\]'
    SEMI = r';'

    # Unary operators
    #OpUnarySoma = r'\+\w+'
    #OpUnarySub = r'-\w+'
    #OPUnaryDif = r'!\w+'  # Assuming this is a unary difference operator





    # Special cases
    def ID(self, t):
      t.type = self.keywords.get(t.value, "ID")
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

    # Internal auxiliary methods
    def _error(self, msg, token):
        location = self._make_location(token)
        self.error_func(msg, location[0], location[1])
        self.index += 1

    def _make_location(self, token):
        return token.lineno, self.find_column(token)

    # Error handling rule
    def error(self, t):
        msg = "Illegal character %s" % repr(t.value[0])
        self._error(msg, t)
    
    def error_char(self, t):
        msg = "Unterminated character const"
        self._error(msg, t)

    def error_comment(self, t):
        msg = "Unterminated comment"
        self._error(msg, t)

    # Scanner (used only for test)
    def scan(self, text):
        output = ""
        for tok in self.tokenize(text):
            print(tok)
            output += str(tok) + "\n"
        return output