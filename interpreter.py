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

def eval_exp(tree, env):
    exptype = tree[0]
    if exptype == "int" or exptype == "double":
        return tree[1]
    elif exptype == "binop":
        op = tree[2]
        left  = eval_exp(tree[1], env)
        right = eval_exp(tree[3], env)
        if   op == '+': return left + right
        elif op == '-': return left - right
        elif op == '*': return left * right
        elif op == '/': return left / right
    elif exptype == "id":
        var_id = tree[1]
        return env_lookup(env, var_id)

def eval_stmt(tree, env):
    stmttype = tree[0]
    if stmttype == "declare":
        _, var_id, var_type, exp = tree
        new_val = eval_exp(exp, env)
        env_declare(env, var_id, new_val)
    elif stmttype == "assign":
        _, var_id, exp = tree
        new_val = eval_exp(exp, env)
        env_update(env, var_id, new_val)
    elif stmttype == "if-else":
        _, condition_exp, then_stmts, else_stmts = tree
        if eval_exp(condition_exp):
            eval_stmts(then_stmts, env)
        else:
            eval_stmts(else_stmts, env)

def eval_stmts(stmts, env):
    for stmt in stmts:
        eval_stmt(stmt, env)

def env_lookup(env, var_id):
    try:
        varType = env[var_id][1]
        env[var_id] = (value, varType)   # making new tuple since tuples immutable
    except LookupError:
        print(f"Undeclared variable name/id {id!r}")

def env_update(env, var_id, new_val):
    env[var_id] = new_val

def print_val(tree):
    if tree is None:
        return
    print(tree)

def interpret(trees):
    'Runs the instructions in the passed Parse Tree'
    if trees is None:
        return
    for tree in trees:
        nodetype = tree[0]
        if type(tree) == tuple:
            if nodetype == 'id':
                return get_value_id(tree[1])
            elif nodetype == 'print':
                print_val(tree[1])
            elif nodetype == 'declare':
                declare_variable(tree[2], interpret(tree[3]), tree[1])
            elif nodetype == 'assign':
                assign_variable(tree[1], interpret(tree[2]))
            # elif nodetype == 'binop':
            #     eval_exp(t)
        # print(variables)
        else:
            return tree

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
