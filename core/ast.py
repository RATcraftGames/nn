class NnNumber:
    def __init__(self, value):
        self.value = value

class NnString:
    def __init__(self, value):
        self.value = value

class NnVariable:
    def __init__(self, name):
        self.name = name

class NnBinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class NnAssign:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class NnEcho:
    def __init__(self, expr):
        self.expr = expr

class NnIf:
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body

class NnWhile:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class NnFunction:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class NnCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args

class NnReturn:
    def __init__(self, expr):
        self.expr = expr

class NnProgram:
    def __init__(self, statements):
        self.statements = statements

def print_ast(node, indent=0):
    """Печатает AST в читаемом виде"""
    if node is None:
        return
    
    prefix = "  " * indent
    
    if isinstance(node, NnProgram):
        print(f"{prefix}Program:")
        for stmt in node.statements:
            print_ast(stmt, indent + 1)
    elif isinstance(node, NnNumber):
        print(f"{prefix}Number: {node.value}")
    elif isinstance(node, NnString):
        print(f"{prefix}String: '{node.value}'")
    elif isinstance(node, NnVariable):
        print(f"{prefix}Variable: {node.name}")
    elif isinstance(node, NnBinOp):
        print(f"{prefix}BinOp: {node.op}")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)
    elif isinstance(node, NnAssign):
        print(f"{prefix}Assign: {node.name}")
        print_ast(node.expr, indent + 1)
    elif isinstance(node, NnEcho):
        print(f"{prefix}Echo:")
        print_ast(node.expr, indent + 1)
    elif isinstance(node, NnIf):
        print(f"{prefix}If:")
        print_ast(node.condition, indent + 1)
        print(f"{prefix}Then:")
        print_ast(node.then_body, indent + 1)
        if node.else_body:
            print(f"{prefix}Else:")
            print_ast(node.else_body, indent + 1)
    elif isinstance(node, NnWhile):
        print(f"{prefix}While:")
        print_ast(node.condition, indent + 1)
        print(f"{prefix}Body:")
        print_ast(node.body, indent + 1)
    elif isinstance(node, NnFunction):
        print(f"{prefix}Function: {node.name}({', '.join(node.params)})")
        print_ast(node.body, indent + 1)
    elif isinstance(node, NnCall):
        print(f"{prefix}Call: {node.name}")
        for arg in node.args:
            print_ast(arg, indent + 1)
    elif isinstance(node, NnReturn):
        print(f"{prefix}Return:")
        print_ast(node.expr, indent + 1)
