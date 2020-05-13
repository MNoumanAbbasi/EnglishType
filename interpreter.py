import ply.yacc as yacc
import parser
import sys
yaplParser = yacc.yacc(module=parser, debug=True)

# Global environment tuple
# value1: parent environment
# value2: current environment dictionary
# Structure of environment dictionary:
# {'myInt' : (5, 'int'), ...}
global_env = (None, { })

def _checkTypeError(value, valType):
    'Raises TypeError if value does not match type'
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
    if exptype == "binop":
        op = tree[2]
        left  = eval_exp(tree[1], env)
        right = eval_exp(tree[3], env)
        if   op == '+': return left + right
        elif op == '-': return left - right
        elif op == '*': return left * right
        elif op == '/': return left / right
    elif exptype == "id":
        var_id = tree[1]
        return env_lookup(env, var_id)[1]
    else:
        return tree[1]

def postfix_op(var_id, postfix, env):
    val = env_lookup(env, var_id)[1]
    try:
        if postfix == "++": val += 1
        if postfix == "--": val -= 1
    except:
        raise Exception('PostfixTypeError')
    env_update(env, var_id, val)

def eval_stmt(tree, env):
    stmttype = tree[0]
    if stmttype == "declare":
        _, var_id, var_type, exp = tree
        new_val = eval_exp(exp, env)
        env_declare(env, var_id, var_type, new_val)
    elif stmttype == "assign":
        _, var_id, exp = tree
        new_val = eval_exp(exp, env)
        env_update(env, var_id, new_val)
    elif stmttype == "print":
        print_val(tree[1], env)
    elif stmttype == "postfix":
        postfix_op(tree[1], tree[2], env)
    elif stmttype == "if-else":
        _, condition_exp, then_stmts, else_stmts = tree
        if eval_exp(condition_exp):
            eval_stmts(then_stmts, env)
        else:
            eval_stmts(else_stmts, env)
    elif stmttype == "exp":
        eval_exp(tree[1], env)

def eval_stmts(stmts, env):
    for stmt in stmts:
        eval_stmt(stmt, env)

def env_declare(env, var_id, var_type, new_val):
    parent_env, curr_env = env
    if var_id in curr_env:
        raise Exception('RedeclarationError')
    else:
        _checkTypeError(new_val, var_type)
        curr_env[var_id] = (var_type, new_val)

def env_lookup(env, var_id):
    parent_env, curr_env = env
    if var_id in curr_env:      # if in current env
        return curr_env[var_id]
    elif parent_env == None:    # if not even in global env
        raise LookupError
    else:                       # else look in parent
        return env_lookup(parent_env, var_id)
    # try:
    #     varType = env[var_id][1]
    #     env[var_id] = (value, varType)   # making new tuple since tuples immutable
    # except LookupError:
    #     print(f"Undeclared variable name/id {id!r}")

def env_update(env, var_id, new_val):
    parent_env, curr_env = env
    if var_id in curr_env:
        var_type = curr_env[var_id][0]
        _checkTypeError(new_val, var_type)
        curr_env[var_id] = (var_type, new_val)
    elif parent_env == None:    # Remove this since lookup already done
        raise LookupError
    else:
        env_update(parent_env, var_id, new_val)


def print_val(args, env):
    for arg in args or []:
        exp = eval_exp(arg, env)
        print(exp, end=' ')
    print()

def interpret(trees):
    'Runs the instructions in the passed Parse Tree'
    # print(trees)
    if trees is None:
        return
    for tree in trees:
        nodetype = tree[0]
        if type(tree) is tuple:
            if nodetype == 'stmt':
                eval_stmt(tree[1], global_env)
        else:
            return tree

def run_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
        try:
            trees = yaplParser.parse(content)
            interpret(trees)
        except Exception as e:
            print('Error:', e)
        # print(content)

def run_terminal():
    while True:
        try:
            s = input('>> ')
        except EOFError:
            break
        if s == 'exit': break
        try:
            trees = yaplParser.parse(s)
            interpret(trees)
        except Exception as e:
            print('Error:', e)
        # print(trees)
        # print(global_env)

def main():
    # print()
    # if text file provided
    if len(sys.argv) == 2:
        filename = 'test_cases/' + sys.argv[1]
        run_file(filename)
    # else open terminal input
    else:
        run_terminal()

if __name__ == "__main__":
    main()
