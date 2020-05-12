import ply.yacc as yacc
from lexer import tokens

# All lines are statements
start = 'statement'

# Precedence rules for the arithmetic operators
precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )

def _checkTypeError(value, valType):
    'Raises typeError if value does not match type'
    if valType == 'int' and not isinstance(value, int):
        raise TypeError
    if valType == 'double' and not isinstance(value, float):
        raise TypeError
    if valType == 'char' and not isinstance(value, str):
        raise TypeError
    if valType == 'string' and not isinstance(value, str):
        raise TypeError
    if valType == 'bool' and not isinstance(value, bool):
        raise TypeError

def p_statement(p):
    '''statement : var_declare
                 | var_assign
                 | empty'''
    p[0] = p[1]

def p_var_declare(p):
    '''var_declare : DECLARE type ID
                   | DECLARE type ID TO value'''
    if len(p) == 6:
        try:
            _checkTypeError(p[5], p[2])
            p[0] = (p[1], p[2], p[3], p[5])
        except TypeError:
            print("TypeError")
    else:
        p[0] = (p[1], p[2], p[3], None)

def p_var_assign(p):
    'var_assign : ASSIGN ID TO value'
    p[0] = (p[1], p[2], p[4])

def p_value_literal(p):
    'value : literal'
    p[0] = p[1]

def p_value_expression(p):
    'value : expression'
    p[0] = p[1]

# def p_value_id(p):
#     'value : ID'
#     try:
#         p[0] = variables[p[1]][0]
#     except LookupError:
#         print(f"Undefined variable name/id {p[1]!r}")
#         p[0] = 0

def p_literal(p):
    '''literal : CHAR
               | STRING
               | BOOL'''
    p[0] = p[1]

def p_number(p):
    '''number : INT
              | DOUBLE'''
    p[0] = p[1]


def p_statement_print(p):
    'statement : PRINT printvalue'
    print(p[2])

def p_printvalue(p):
    '''printvalue : value printvalue
                  | value'''
    p[0] = str(p[1]) + " " + (str(p[2]) if len(p) == 3 else "")

def p_empty(p):
    'empty :'
    p[0] = None
# def p_statement_value(p):
#     'statement : value'
#     print(p[1])


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
    # print(f"Syntax error")
    print(f"Syntax error at {p.value!r}")
