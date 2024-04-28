class UCyanLexer(Lexer):
    """A lexer for the uCyan language."""

    def __init__(self, error_func):
        """Create a new Lexer.
        An error function. Will be called with an error
        message, line and column as arguments, in case of
        an error during lexing.
        """
        self.error_func = error_func
        self.last_cr = 0  # Initialize last_cr to avoid errors

    # Reserved keywords
    keywords = {
        'print': "PRINT",
        'if': "IF",
        'else': "ELSE",
        'while': "WHILE",
        'break': "BREAK",
        'continue': "CONTINUE",
        'let': "LET",
        'var': "VAR",
        'int': "ID",
        'float': "ID",
        'char': "ID",
        'true': "TRUE",
        'false': "OpLogFalse",
    }

    # All the tokens recognized by the lexer
    tokens = tuple(keywords.values()) + (
        # Identifiers
        "ID",
        # Delimeters
        "SEMI",
        "LPAREN",
        "RPAREN",
        "LBRACE",
        "RBRACE",
        # Constants
        "FLOAT_CONST",
        "INT_CONST",
        "CHAR_CONST",
        # Operators
        "EQ",
        "PLUS",
        "MINUS",
        "TIMES",
        "DIVIDE",
        "LT",
        "OpRelMenorIgual",
        "GT",
        "OpRelMaiorIgual",
        "OpRelDif",
        "AND",
        "OpLogOu",
        # Unitary Operators
        "OpUnarySoma",
        "OpUnarySub",
        "OPUnaryDif",
        # Assignment
        "UNCOMMENT",
        "EQUALS",
    )

    # String containing ignored characters (between tokens)
    ignore = " \t"

    # Other ignored patterns
    ignore_newline = r'\n+'
    #ignore_uncomment = r'\/\*.*?\*\/'
    ignore_multiline = r'\/\*(.|\n)*?\*\/'
    ignore_comment = r'\/\/.*'

    # Delimitadores
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACE = r'\{|\['
    RBRACE = r'\}|\]'
    SEMI = r';|:'

    # Regular expression rules for tokens
    ID = r'[a-zA-Z][a-zA-Z0-9]*'
    FLOAT_CONST = r'\d+\.\d+'
    INT_CONST = r'\d+'
    CHAR_CONST = r'\'([^\\\n]|(\\.))*?\''

    # Binary operators
    AND = r'\&\&'
    EQ = r'=='
    OpRelDif = r'<>'
    OpRelMenorIgual = r'<='
    OpRelMaiorIgual = r'>='
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'\/'
    LT = r'<'
    GT = r'>'

    # Unary operators
    OpUnarySoma = r'\+'
    OpUnarySub = r'-'
    OPUnaryDif = r'!'  # Assuming this is a unary difference operator

    UNCOMMENT = r'\/\*(?:[^*]|\*(?!\/))*\*\/'



    EQUALS = r'='

    # Special cases
    def ID(self, t):
        t.type = self.keywords.get(t.value, "ID")
        return t

    def INT_CONST(self, t):
        # t.value = int(t.value)
        return t

    def FLOAT_CONST(self, t):
        # t.value = float(t.value)  # Convert to float
        return t

    # Define a rule so we can track line numbers
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def ignore_comment(self, t):
        self.lineno += t.value.count("\n")

    def ignore_multiline(self, t):
      self.lineno += t.value.count("\n")

    #def UNCOMMENT(self, t):
        #self.lineno += t.value.count("\n")

    #def ignore_line_comment(self, t):
        #pass  # No action needed for line comments

    def find_column(self, token):
        """Find the column of the token in its line."""
        last_cr = self.text.rfind('\n', 0, token.index)
        if last_cr < 0:
            last_cr = 0
        column = (token.index - last_cr)
        return column

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
        self.index += 1

    # Scanner (used only for test)
    def scan(self, text):
        output = ""
        for tok in self.tokenize(text):
            if tok.type not in ('COMMENT', 'UNCOMMENT', 'LINE_COMMENT'):
                print(tok)
                output += str(tok) + "\n"
        return output

    # Define uma função de tratamento de erro
    def error_func(msg, line, column):
        print(f"Erro na linha {line}, coluna {column}: {msg}")
