import ply.yacc as yacc
from parser import _checkTypeError
import parser
yaplParser = yacc.yacc(module=parser)


# Dictionary of variable
# key: identifier/name
# value: tuple of literal value and type
# e.g. 'myInt' : (5, 'int')
variables = { }

def declare_variable(id, value, typ):
    if id in variables:
        print('RedeclarationError')
        return            
    variables[id] = (value, typ)

def assign_variable(id, value):
    try:
        varType = variables[id][1]
        print(value, varType)
        _checkTypeError(value, varType)
        variables[id] = (value, varType)   # making new tuple since tuples immutable
    except LookupError:
        print(f"Undeclared variable name/id {id!r}")
    except TypeError:
        print("TypeError")


def run(tree):
    if type(tree) == tuple:
        if tree[0] == 'declare':
            declare_variable(tree[2], tree[3], tree[1])
        if tree[0] == 'assign':
            assign_variable(tree[1], tree[2])
        print(variables)


while True:
    try:
        s = input('>> ')
    except EOFError:
        break
    tree = yaplParser.parse(s)
    # print(tree)
    run(tree)