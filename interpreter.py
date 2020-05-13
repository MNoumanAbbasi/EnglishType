import ply.yacc as yacc
import parser
import sys
yaplParser = yacc.yacc(module=parser, debug=True)

# Dictionary of variable
# key: identifier/name
# value: tuple of literal value and type
# e.g. 'myInt' : (5, 'int')
variables = { }

env = {}

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

def eval_exp(tree, env):
    nodetype = tree[0]
    if nodetype == "int" or nodetype == "double":
        return tree[1]
    elif nodetype == "binop":
        op = tree[2]
        left  = eval_exp(tree[1], env)
        right = eval_exp(tree[3], env)
        if   op == '+': return left + right
        elif op == '-': return left - right
        elif op == '*': return left * right
        elif op == '/': return left / right
    elif nodetype == "id":
        var_id = tree[1]
        return env_lookup(env, var_id)

def env_lookup(env, var_id):
    pass

def print_val(tree):
    print(tree)

def interpret(trees):
    'Runs the instructions in the passed Parse Tree'
    if trees is None:
        return
    for t in trees:
        nodetype = t[0]
        if type(t) == tuple:
            if nodetype == 'id':
                return get_value_id(t[1])
            elif nodetype == 'print':
                print_val(t[1])
            elif nodetype == 'declare':
                declare_variable(t[2], interpret(t[3]), t[1])
            elif nodetype == 'assign':
                assign_variable(t[1], interpret(t[2]))
            # elif nodetype == 'binop':
            #     eval_exp(t)
        # print(variables)
        else:
            return t

def run_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
        try:
            trees = yaplParser.parse(content)
        except Exception as e:
            print(e)
        # print(content)
        interpret(trees)

def run_terminal():
    while True:
        try:
            s = input('>> ')
        except EOFError:
            break
        if s == 'exit': break
        trees = yaplParser.parse(s)
        # print(trees)
        interpret(trees)

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
