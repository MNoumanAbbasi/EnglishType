import ply.lex as lex
import sys
# Reserved keywords
keywords = {
    'declare' : 'DECLARE',
    'set' : 'SET',
    'print' : 'PRINT',
    'int' : 'INT_TYPE',
    'double' : 'DOUBLE_TYPE',
    'char' : 'CHAR_TYPE',
    'string' : 'STRING_TYPE',
    'bool' : 'BOOL_TYPE',
    'to' : 'TO',
    'if' : 'IF',
    'else' : 'ELSE',
}

# List of tokens types
tokens = [
    'ID',
    'INT', 'DOUBLE', 'CHAR', 'STRING', 'BOOL',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    # 'INCREM', 'DECREM',
    'LPAREN','RPAREN',
    'SEMICL', 'OPENBR', 'CLSEBR', 'COMMA',
 ] + list(keywords.values())


# Tokens
# t_INCREM = r'\+\+'
# t_DECREM = r'--'
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICL = r'\;'
t_OPENBR = r'{'
t_CLSEBR = r'}'
t_COMMA  = r','

def t_BOOL(t):
    r'True|False'
    t.value = True if t.value == 'True' else False
    return t

# t_ID   = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_DOUBLE(t):
    r'[+-]?([0-9]*)?[.][0-9]+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'[+-]?[0-9]+'
    t.value = int(t.value)
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
t_ignore = ' \t\v\r'

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
assign myint 5,5 else to 5+ ;5++{}
'''

# Give the lexer some input
# lexer.input(data2)
# filename = 'test_cases/' + sys.argv[1]
# with open(filename, 'r') as file:
#     content = file.read()
#     lexer.input(content)

# for tok in lexer:
#     print(tok)
