import ply.yacc as yacc
import parser
import sys
yaplParser = yacc.yacc(module=parser)

# Dictionary of variable
# key: identifier/name
# value: tuple of literal value and type
# e.g. 'myInt' : (5, 'int')
variables = { }

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


def get_value_id(id):
    try:
        return variables[id][0]
    except LookupError:
        print(f"Undefined variable name/id {p[1]!r}")
        return 0


def declare_variable(id, value, typ):
    if id in variables:
        print('RedeclarationError')
        return
    try:
        _checkTypeError(value, typ)
        variables[id] = (value, typ)
    except TypeError:
        print("TypeError")

def assign_variable(id, value):
    try:
        varType = variables[id][1]
        _checkTypeError(value, varType)
        variables[id] = (value, varType)   # making new tuple since tuples immutable
    except LookupError:
        print(f"Undeclared variable name/id {id!r}")
    except TypeError:
        print("TypeError")


def interpret(pt):
    'Runs the instructions in the passed Parse Tree'
    # print(pt)
    if type(pt) == tuple:
        if pt[0] == 'id':
            return get_value_id(pt[1])
        elif pt[0] == 'print':
            print(interpret(pt[1]))
        elif pt[0] == 'declare':
            declare_variable(pt[2], interpret(pt[3]), pt[1])
        elif pt[0] == 'assign':
            assign_variable(pt[1], interpret(pt[2]))
        # print(variables)
    else:
        return pt


# while True:
#     try:
#         s = input('>> ')
#     except EOFError:
#         break
#     tree = yaplParser.parse(s)
#     # print(tree)
#     interpret(tree)

filename = 'test_cases/' + sys.argv[1]
with open(filename, 'r') as file:
    content = file.read()
    tree = yaplParser.parse(content)
    # print(content)
    interpret(tree)