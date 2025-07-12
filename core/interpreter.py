from core.ast import *

class Environment:
    def __init__(self, parent=None):
        self.variables = {}
        self.functions = {}
        self.parent = parent

    def set_var(self, name, value):
        self.variables[name] = value

    def get_var(self, name):
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get_var(name)
        raise NameError(f"Переменная '{name}' не определена")

    def set_func(self, name, func):
        self.functions[name] = func

    def get_func(self, name):
        if name in self.functions:
            return self.functions[name]
        if self.parent:
            return self.parent.get_func(name)
        raise NameError(f"Функция '{name}' не определена")

class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.setup_builtins()

    def setup_builtins(self):
        self.global_env.set_func("print", lambda *args: print(*args))
        self.global_env.set_func("input", lambda prompt="": input(prompt))

    def interpret(self, node, env=None):
        if env is None:
            env = self.global_env

        if isinstance(node, NnProgram):
            result = None
            for stmt in node.statements:
                result = self.interpret(stmt, env)
            return result

        elif isinstance(node, NnNumber):
            return node.value

        elif isinstance(node, NnString):
            return node.value

        elif isinstance(node, NnVariable):
            return env.get_var(node.name)

        elif isinstance(node, NnBinOp):
            left = self.interpret(node.left, env)
            right = self.interpret(node.right, env)
            
            if node.op == '+':
                # Если хотя бы один из операндов строка — приводим оба к строке
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                return left + right
            elif node.op == '-':
                return left - right
            elif node.op == '*':
                return left * right
            elif node.op == '/':
                if right == 0:
                    raise ZeroDivisionError("Деление на ноль!")
                return left / right
            elif node.op == '==':
                return left == right
            elif node.op == '!=':
                return left != right
            elif node.op == '<':
                return left < right
            elif node.op == '<=':
                return left <= right
            elif node.op == '>':
                return left > right
            elif node.op == '>=':
                return left >= right
            elif node.op == '&&':
                return bool(left and right)
            elif node.op == '||':
                return bool(left or right)
            else:
                raise ValueError(f"Неизвестный оператор: {node.op}")

        elif isinstance(node, NnAssign):
            value = self.interpret(node.expr, env)
            env.set_var(node.name, value)
            return value

        elif isinstance(node, NnEcho):
            value = self.interpret(node.expr, env)
            print(value)
            return value

        elif isinstance(node, NnIf):
            condition = self.interpret(node.condition, env)
            if condition:
                return self.interpret(node.then_body, env)
            elif node.else_body:
                return self.interpret(node.else_body, env)
            return None

        elif isinstance(node, NnWhile):
            while self.interpret(node.condition, env):
                self.interpret(node.body, env)
            return None

        elif isinstance(node, NnFunction):
            env.set_func(node.name, (node.params, node.body))
            return None

        elif isinstance(node, NnCall):
            func = env.get_func(node.name)
            if callable(func):
                args = [self.interpret(arg, env) for arg in node.args]
                return func(*args)
            else:
                params, body = func
                if len(params) != len(node.args):
                    raise TypeError(f"Функция {node.name} ожидает {len(params)} аргументов, получено {len(node.args)}")
                
                new_env = Environment(env)
                for param, arg in zip(params, node.args):
                    new_env.set_var(param, self.interpret(arg, env))
                
                return self.interpret(body, new_env)

        elif isinstance(node, NnReturn):
            value = self.interpret(node.expr, env)
            raise ReturnValue(value)

        elif isinstance(node, list):
            result = None
            for stmt in node:
                result = self.interpret(stmt, env)
            return result

        else:
            raise ValueError(f"Неизвестный тип узла: {type(node)}")

class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value
        super().__init__()

def run_interpreter(ast):
    interpreter = Interpreter()
    try:
        return interpreter.interpret(ast)
    except ReturnValue as rv:
        return rv.value
