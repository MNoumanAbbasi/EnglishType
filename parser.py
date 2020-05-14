import ply.yacc as yacc
from lexer import tokens

# All lines are statements
start = 'statements'

# Precedence rules for the operators
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'EQ', 'NOTEQ', 'LT', 'GT', 'LTE', 'GTE'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE','MOD'),
    ('right','UMINUS'),
    ('right', 'POWER'),
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
                 | list_declare SEMICL
                 | print_val SEMICL
                 | inc_dec SEMICL
                 | expression SEMICL
                 | if_elif_else'''
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

def p_list_declare(p):
    '''list_declare : DECLARE LIST ID
                    | DECLARE LIST ID TO expression'''
    if len(p) == 6:
        p[0] = ('declare-list', p[3], p[2].lower(), p[5])
    else:
        p[0] = ('declare-list', p[3], p[2].lower(), ('list', []))

def p_expression_list(p):
    'expression : LISTOP args LISTCL'
    p[0] = ('list', p[2])

# def p_list_assign(p):
#     '''list_assign : SET ID TO expression'''
#     p[0] = ('assign-list', p[2], p[5])

# def p_expression_list_op(p):
#     'expression : list_pop'
#     p[0] = ('list-op', p[1])

def p_list_pop(p):
    'expression : expression POP INT'
    p[0] = ('pop-list', p[1], p[3])

def p_print_val(p):
    'print_val : PRINT args'
    # args are a list of arguments (tuples)
    p[0] = ('print', p[2])

def p_args(p):
    '''args : args COMMA expression
            | expression'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_inc_dec(p):
    '''inc_dec : ID INCREM
               | ID DECREM'''
    p[0] = ('postfix', p[1], p[2])


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

def p_expression_id(p):
    'expression : ID'
    p[0] = ('id', p[1])

# def p_id(p):
#     'id : ID'
#     p[0] = ('id', p[1])

def p_if_elif_else(p):
    '''if_elif_else : IF expression scope elifstatements elsestatement
                    | IF expression scope elifstatements
                    | IF expression scope elsestatement
                    | IF expression scope'''
    # if len(p) == 4:
    # elif len(p) == 6:
    if len(p) == 4:
        p[0] = ('if-elif-else', [(p[2], p[3])])
    if len(p) == 5:
        p[0] = ('if-elif-else', [(p[2], p[3])] + p[4])
    if len(p) == 6:
        p[0] = ('if-elif-else', [(p[2], p[3])] + p[4] + p[5])
    # print(p[0])
# def p_if(p):
#     'ifstatement : IF expression scope'
#     p[0] = ('if', p[2], p[3])

def p_elif(p):
    '''elifstatements : ELSEIF expression scope elifstatements
                      | ELSEIF expression scope'''
    if len(p) == 5:
        p[0] = [(p[2], p[3])] + p[4]
    else:
        p[0] = [(p[2], p[3])]

def p_else(p):
    '''elsestatement : ELSE scope'''
    if len(p) == 3:
        p[0] = [(('bool', True), p[2])]
    else:
        p[0] = []

def p_scope(p):
    '''scope : OPENBR statements CLSEBR
             | OPENBR scope CLSEBR'''
    p[0] = p[2]
    # print(p[0])

# def p_number(p):
#     '''number : INT
#               | DOUBLE'''
#     p[0] = p[1]

def p_empty(p):
    'empty :'
    p[0] = None

def p_type(p):
    '''type : INT_TYPE
            | DOUBLE_TYPE
            | CHAR_TYPE
            | STRING_TYPE
            | BOOL_TYPE'''
    p[0] = p[1].lower()

# def p_statement_expr(p):
#     'statement : expression'
#     print(p[1])
def p_expression_logop(p):
    '''expression : expression LT expression
                  | expression GT expression
                  | expression LTE expression
                  | expression GTE expression
                  | expression NOTEQ expression
                  | expression EQ expression
                  | expression AND expression
                  | expression OR expression'''
    p[0] = ('logop', p[1], p[2], p[3])

def p_expression_not(p):
    'expression : NOT expression'
    p[0] = ('not', p[2])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression POWER expression
                  | expression MOD expression'''
    p[0] = ('binop', p[1], p[2], p[3])

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = ('unary', p[2])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

# def p_expression_number(p):
#     'expression : number'
#     p[0] = p[1]

def p_error(p):
    if p:
        print(f"Syntax error at {p.value!r}")
        # raise Exception(f"Syntax error at {p.value!r}")
    else:
        raise Exception(f"Syntax error")
