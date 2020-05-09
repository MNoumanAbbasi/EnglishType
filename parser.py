import ply.yacc as yacc
from lexer import tokens

# Precedence rules for the arithmetic operators
precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )

# dictionary of names (for storing variables)
names = { }

def p_statement_declare(p):
    '''statement : DECLARE type NAME
                 | DECLARE type NAME TO value'''
    if p[3] in names:
        print('RedeclarationError')
        return

    value = None
    try:
        if len(p) == 6:
            value = int(p[5])   if p[2] == 'int' else value
            value = float(p[5]) if p[2] == 'double' else value
            value = chr(p[5])   if p[2] == 'char' else value
            value = str(p[5])   if p[2] == 'string' else value
            value = bool(p[5])  if p[2] == 'bool' else value
        names[p[3]] = (value, p[2])
    except:
        print('TypeError')

def p_value_expression(p):
    '''value : expression
             | NAME'''
    p[0] = p[1]

def p_statement_display(p):
    '''statement : 

def p_statement_value(p):
    'statement : value'
    print(p[1])

def p_statement_assign(p):
    'statement : NAME EQUALS expression'
    names[p[1]] = p[3]

def p_type_datatype(p):
    '''type : INT
            | DOUBLE
            | CHAR
            | STRING
            | BOOL'''
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
    'expression : NUMBER'
    p[0] = p[1]

# def p_expression_name(p):
#     'expression : NAME'
#     try:
#         p[0] = names[p[1]]
#     except LookupError:
#         print(f"Undefined name {p[1]!r}")
#         p[0] = 0

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