import ply.yacc as yacc
from lexer import tokens

# All lines are statements
start = 'statements'

# Precedence rules for the arithmetic operators
precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )

def p_statements(p):
    '''statements : statements statement
                  | statement
                  | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement(p):
    '''statement : var_declare SEMICL
                 | var_assign SEMICL
                 | print_val SEMICL
                 | inc_dec SEMICL'''
    p[0] = ('stmt', p[1])

def p_var_declare(p):
    '''var_declare : DECLARE type ID
                   | DECLARE type ID TO expression'''
    if len(p) == 6:
        p[0] = ('declare', p[3], p[2], p[5])
    else:
        p[0] = ('declare', p[3], p[2], None)

def p_var_assign(p):
    'var_assign : SET ID TO expression'
    p[0] = ('assign', p[2], p[4])

def p_print_val(p):
    'print_val : PRINT args'
    # args are a list of arguments (tuples)
    p[0] = ('print', p[2])

def p_inc_dec(p):
    '''inc_dec : ID INCREM
               | ID DECREM'''
    p[0] = ('postfix', p[1], p[2])
    print(p[0])

def p_args(p):
    '''args : args COMMA expression
            | expression'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_expression_int(p):
    'expression : INT'
    p[0] = ('int', p[1])

def p_expression_double(p):
    'expression : DOUBLE'
    p[0] = ('double', p[1])

def p_expression_char(p):
    'expression : CHAR'
    p[0] = ('char', p[1])

def p_expression_string(p):
    'expression : STRING'
    p[0] = ('string', p[1])

def p_expression_bool(p):
    'expression : BOOL'
    p[0] = ('bool', p[1])

# def p_value_expression(p):
#     'value : expression'
#     p[0] = p[1]

def p_expression_id(p):
    'expression : ID'
    p[0] = ('id', p[1])

def p_if_else(p):
    '''statements : IF expression OPENBR statements CLSEBR
                  | IF expression OPENBR statements CLSEBR ELSE OPENBR statements CLSEBR'''
    if len(p) == 10:
        p[0] = ('if-else', p[2], p[4], p[8])
    else:
        p[0] = ('if-else', p[2], p[4], None)
# def p_literal(p):
#     '''literal : CHAR
#                | STRING
#                | BOOL'''
#     p[0] = p[1]

# def p_number(p):
#     '''number : INT
#               | DOUBLE'''
#     p[0] = p[1]

# args is a list of tuples

# def p_printvalue(p):
#     '''printvalue : expression printvalue
#                   | expression'''
#     p[0] = str(p[1]) + (" " + str(p[2]) if len(p) == 3 else "")

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
    p[0] = ('binop', p[1], p[2], p[3])

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

# def p_expression_number(p):
#     'expression : number'
#     p[0] = p[1]

def p_error(p):
    try:
        print(f"Syntax error at {p.value!r}")
    except:
        print(f"Syntax error")
