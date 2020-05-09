import ply.lex as lex

# Reserved keywords
reserved = {
    'declare' : 'DECLARE',
    'display' : 'DISPLAY',
    'int' : 'INT',
    'double' : 'DOUBLE',
    'char' : 'CHAR',
    'string' : 'STRING',
    'bool' : 'BOOL',
    'to' : 'TO',
}

# List of tokens types
tokens = [
    'NAME','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN', 'RESERVE',
 ] + list(reserved.values())


# Tokens
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NAME   = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"(.+?)\"'
    t.value = str(t.value[1:-1])
    return t

def t_CHAR(t):
    r'\'(.+?)\''
    t.value = str(t.value[1:-1])
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# token specfication for reserved keywords
def t_RESERVE(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'NAME')
    return t

def t_error(t):
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
data = '''
3 + 4 * 10
  + -20 *2
'''
data2 = '''
"5"
declare int myInt
declare int x to 5.2
'''

# Give the lexer some input
lexer.input(data2)

for tok in lexer:
    print(tok)
