import ply.lex as lex

# Reserved keywords
keywords = {
    'declare' : 'DECLARE',
    'display' : 'DISPLAY',
    'int' : 'INT_TYPE',
    'double' : 'DOUBLE_TYPE',
    'char' : 'CHAR_TYPE',
    'string' : 'STRING_TYPE',
    'bool' : 'BOOL_TYPE',
    'to' : 'TO',
}

# List of tokens types
tokens = [
    'ID','LITERAL',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN',
    'INT', 'DOUBLE', 'CHAR', 'STRING', 'BOOL',
 ] + list(keywords.values())


# Tokens
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_BOOL(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return t

# t_ID   = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_INT(t):
    r'[+-]?[0-9]+'
    t.value = int(t.value)
    return t

def t_DOUBLE(t):
    r'[+-]?([0-9]*[.])?[0-9]+'
    t.value = float(t.value)
    return t

def t_CHAR(t):
    r'\'(.+?)\''
    t.value = str(t.value[1:-1])
    return t

def t_STRING(t):
    r'\"(.+?)\"'
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
    t.type = keywords.get(t.value, 'ID')
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
true false
myint int
'''

# Give the lexer some input
lexer.input(data2)

for tok in lexer:
    print(tok)

# if r'^true$/' == 
#     print("OK")
