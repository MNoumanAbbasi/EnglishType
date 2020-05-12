import ply.yacc as yacc
import parser
yaplParser = yacc.yacc(module=parser)


# Dictionary of variable
# key: identifier/name
# value: tuple of literal value and type
# e.g. 'myInt' : (5, 'int')
variables = { }



def declare_variable(id, typ, value):
    if id in variables:
        print('RedeclarationError')
        return            
    variables[id] = (value, typ)

def run(tree):
    print(tree)
    if type(tree) == tuple:
        if tree[0] == 'declare':
            declare_variable(tree[2], tree[1], tree[3])
            print(variables)


while True:
    try:
        s = input('>> ')
    except EOFError:
        break
    tree = yaplParser.parse(s)
    # print(tree)
    run(tree)