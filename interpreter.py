import ply.yacc as yacc
import parser
yaplParser = yacc.yacc()
# Precedence rules for the arithmetic operators
precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )

# Dictionary of variable
# key: identifier/name
# value: tuple of literal value and type
# e.g. 'myInt' : (5, 'int')
variables = { }


def p_statement(p):
    '''statement : var_declare'''
                #  | empty'''
    run(p)
    print(variables)

def declare_variable(id, typ, value):
    if id in variables:
        print('RedeclarationError')
        return            
    variables[id] = (value, typ)

def run(p):
    if type(p) == tuple:
        if p[0] == 'DECLARE':
            declare_variable(p[2], p[1], p[3])

while True:
    try:
        s = input('>> ')
    except EOFError:
        break
    yaplParser.parse(s)