import ply.yacc as yacc
from lexer import tokens

# TODO: Declare and assign don't perform type checking

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

def p_statement_declare(p):
    '''statement : DECLARE type ID
                 | DECLARE type ID TO value'''
    if p[3] in variables:
        print('RedeclarationError')
        return

    value = None
    if len(p) == 6:
        value = p[5]
        # if type(value) != p[2]:
        #     pass
        # value = int(p[5])   if p[2] == 'int' else value
        # value = float(p[5]) if p[2] == 'double' else value
        # value = chr(p[5])   if p[2] == 'char' else value
        # value = str(p[5])   if p[2] == 'string' else value
        # value = bool(p[5])  if p[2] == 'bool' else value
    variables[p[3]] = (value, p[2])
    # print('TypeError')
    # print(type(value))
    print(variables)

def p_value_literal(p):
    'value : literal'
    p[0] = p[1]

def p_value_id(p):
    'value : ID'
    try:
        p[0] = variables[p[1]][0]
    except LookupError:
        print(f"Undefined variable name/id {p[1]!r}")
        p[0] = 0

def p_literal(p):
    '''literal : number
               | CHAR
               | STRING
               | BOOL'''
    p[0] = p[1]

def p_number(p):
    '''number : INT
              | DOUBLE'''
    p[0] = p[1]


def p_statement_display(p):
    'statement : DISPLAY value'
    print(p[2])

# def p_statement_value(p):
#     'statement : value'
#     print(p[1])

def p_statement_assign(p):
    'statement : ASSIGN ID TO value'
    try:
        varType = variables[p[2]][1]
        variables[p[2]] = (p[4], varType)   # making new tuple since tuples immutable
    except LookupError:
        print(f"Undeclared variable name/id {p[2]!r}")
    print(variables)

def p_type_datatype(p):
    '''type : INT_TYPE
            | DOUBLE_TYPE
            | CHAR_TYPE
            | STRING_TYPE
            | BOOL_TYPE'''
    p[0] = p[1]

# def p_statement_expr(p):
#     'statement : expression'
#     print(p[1])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if p[2] == '+'  : p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : number'
    p[0] = p[1]


def p_error(p):
    print(f"Syntax error")
    # print(f"Syntax error at {p.value!r}")

yacc.yacc()

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    yacc.parse(s)