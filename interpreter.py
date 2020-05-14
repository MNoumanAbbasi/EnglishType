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
        raise Exception("TypeError")
    if valType == 'double' and not isinstance(value, float):
        raise Exception("TypeError")
    if valType == 'char' and not isinstance(value, str):
        raise Exception("TypeError")
    if valType == 'string' and not isinstance(value, str):
        raise Exception("TypeError")
    if valType == 'bool' and not isinstance(value, (bool, int)):
        raise Exception("TypeError")
    if valType == 'list' and not isinstance(value, list):
        raise Exception("TypeError")

def eval_exp(tree, env):
    exptype = tree[0]
    if exptype == "unary":
        return -eval_exp(tree[1], env)
    elif exptype == "not":
        return not eval_exp(tree[1], env)
    elif exptype == "binop":
        op = tree[2]
        left  = eval_exp(tree[1], env)
        right = eval_exp(tree[3], env)
        try:
            if   op == '+': return left + right
            elif op == '-': return left - right
            elif op == '*': return left * right
            elif op == '/': return left / right
            elif op == '^': return left ** right
            elif op == '%': return left % right
        except:
            raise Exception("TypeError")
    elif exptype == "logop":
        op = tree[2]
        left  = eval_exp(tree[1], env)
        right = eval_exp(tree[3], env)
        if   op == '<': return left < right
        elif op == '>': return left > right
        elif op == '<=': return left <= right
        elif op == '>=': return left >= right
        elif op == 'NOTEQUALS': return left != right
        elif op == 'EQUALS': return left == right
        elif op == 'AND': return left and right
        elif op == 'OR': return left or right
    elif exptype == "id":
        var_id = tree[1]
        return env_lookup(env, var_id)[1]
    elif exptype == "list":
        return [eval_exp(v, env) for v in tree[1]]
    elif exptype == "pop-list":
        lst = eval_exp(tree[1], env)
        pop_val = lst.pop(tree[2])
        env_update(env, tree[1][1], lst)
        return pop_val
    elif exptype == "slice-list":
        lst = eval_exp(tree[1], env)
        return lst[tree[2]: tree[3]]
    elif exptype == "index-list":
        lst = eval_exp(tree[1], env)
        return lst[tree[2]]
    elif exptype == "push-list":
        lst = eval_exp(tree[1], env)
        lst.append(eval_exp(tree[2], env))
        env_update(env, tree[1][1], lst)
    else:
        return tree[1]

def postfix_op(var_id, postfix, env):
    val = env_lookup(env, var_id)[1]
    try:
        if postfix == "++": val += 1
        if postfix == "--": val -= 1
    except:
        print("PostfixTypeError")
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
    elif stmttype == "declare-list":
        _, list_id, list_type, value_exps = tree
        values = eval_exp(value_exps, env)
        env_declare(env, list_id, list_type, values)
    # elif stmttype == "assign-list":
    #     _, list_id, value_exps = tree
    #     values = [eval_exp(v, env) for v in value_exps]
    #     env_update(env, list_id, values)
    # elif stmttype == "list-op":
    #     _, list_op = tree
    #     eval_exp(list_op, env)
        # env_update(env, )
    elif stmttype == "print":
        print_val(tree[1], env)
    elif stmttype == "postfix":
        postfix_op(tree[1], tree[2], env)
    elif stmttype == "if-elif-else":
        _, if_stmts = tree
        for (condition_exp, then_stmts) in if_stmts:
            if eval_exp(condition_exp, env):
                eval_stmts(then_stmts, env)
                break
    else:
        eval_exp(tree, env)

def eval_stmts(stmts, env):
    for stmt in stmts:
        eval_stmt(stmt[1], env)

def env_declare(env, var_id, var_type, new_val):
    parent_env, curr_env = env
    if var_id in curr_env:
        # print('RedeclarationError')
        raise Exception('RedeclarationError')
    else:
        #     values = []
        #     for val in new_val:
        # if var_type != "list":
        _checkTypeError(new_val, var_type)
        curr_env[var_id] = (var_type, new_val)

def env_lookup(env, var_id):
    parent_env, curr_env = env
    if var_id in curr_env:      # if in current env
        return curr_env[var_id]
    elif parent_env == None:    # if not even in global env
        # print('LookupError')
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
        # if var_type != "list":
        _checkTypeError(new_val, var_type)
        curr_env[var_id] = (var_type, new_val)
    elif parent_env == None:    # Remove this since lookup already done
        print('LookupError')
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
            print('ERROR:', e)
        # print(content)
        # print(global_env)

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
            print('ERROR:', e)
            break
        # print(trees)
        # print(global_env)

def main():
    print("Welcome to EnglishType Interpreter v0.2!")
    print("OUTPUT:")
    # if text file provided
    if len(sys.argv) == 2:
        filename = 'test_cases/' + sys.argv[1]
        run_file(filename)
    # else open terminal input
    else:
        run_terminal()

if __name__ == "__main__":
    main()
