import ply.yacc as yacc
import parser
import sys
yaplParser = yacc.yacc(module=parser, debug=True)

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

def eval_exp(tree):
    nodetype = tree[0]
    if nodetype == "int" or nodetype == "double":
        return tree[1]
    # elif nodetype == "binop":

def interpret(trees):
    'Runs the instructions in the passed Parse Tree'
    for t in trees:
        print(t)
        if type(t) == tuple:    # t[0]: nodetype
            if t[0] == 'id':
                return get_value_id(t[1])
            elif t[0] == 'print':
                print(interpret(t[1]))
            elif t[0] == 'declare':
                declare_variable(t[2], interpret(t[3]), t[1])
            elif t[0] == 'assign':
                assign_variable(t[1], interpret(t[2]))
        # print(variables)
    else:
        return t

def run_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
        trees = yaplParser.parse(content)
        # print(content)
        interpret(trees)

def run_terminal():
    while True:
        try:
            s = input('>> ')
        except EOFError:
            break
        if s == 'exit': break
        tree = yaplParser.parse(s)
        # print(tree)
        interpret(tree)

def main():
    # if text file provided
    if len(sys.argv) == 2:
        filename = 'test_cases/' + sys.argv[1]
        run_file(filename)
    # else open terminal input
    else:
        run_terminal()

if __name__ == "__main__":
    main()
