import ply.lex as lex
import sys
# Reserved keywords
keywords = {
    'DECLARE' : 'DECLARE',
    'SET' : 'SET',
    'PRINT' : 'PRINT',
    'INT' : 'INT_TYPE',
    'DOUBLE' : 'DOUBLE_TYPE',
    'CHAR' : 'CHAR_TYPE',
    'STRING' : 'STRING_TYPE',
    'BOOL' : 'BOOL_TYPE',
    'LIST' : 'LIST',
    'TO' : 'TO',
    'IF' : 'IF',
    'ELSE' : 'ELSE',
    'ELSEIF': 'ELSEIF',
}

numerical_ops = ['PLUS','MINUS','TIMES','DIVIDE','POWER', 'MOD']
logical_ops = [
    'LT', 'GT', 'LTE', 'GTE', 'NOTEQ', 'EQ',
    'NOT', 'AND', 'OR',
]

# List of tokens types
tokens = [
    'ID',
    'INT', 'DOUBLE', 'CHAR', 'STRING', 'BOOL',
    'INCREM', 'DECREM',
    'LPAREN','RPAREN',
    'SEMICL', 'OPENBR', 'CLSEBR', 'COMMA',
    'LISTOP', 'LISTCL',
 ] + list(keywords.values()) + numerical_ops + logical_ops



# Tokens
t_INCREM = r'\+\+'
t_DECREM = r'--'
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_POWER  = r'\^'
t_MOD    = r'%'
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_SEMICL = r'\;'
t_OPENBR = r'{'
t_CLSEBR = r'}'
t_COMMA  = r','
t_LISTOP = r'\['
t_LISTCL = r'\]'

t_LT     = r'<'
t_GT     = r'>'
t_LTE    = r'<='
t_GTE    = r'>='

def t_NOTEQ(t):
    r'NOTEQUALS'
    return t
def t_EQ(t):
    r'EQUALS'
    return t
def t_NOT(t):
    r'NOT'
    return t
def t_AND(t):
    r'AND'
    return t
def t_OR(t):
    r'OR'
    return t

def t_BOOL(t):
    r'True|False'
    t.value = True if t.value == 'True' else False
    return t

# t_ID   = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_DOUBLE(t):
    r'([0-9]*)?[.][0-9]+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'[0-9]+'
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
DECLARE LIST I TO [5];
'''

# Give the lexer some input
# filename = 'test_cases/' + sys.argv[1]
# with open(filename, 'r') as file:
#     content = file.read()
#     lexer.input(content)

# lexer.input(data2)
# for tok in lexer:
#     print(tok)
