from core.ast import (
    NnAssign,
    NnBinOp,
    NnNumber,
    NnString,
    NnProgram,
    NnVariable,
    NnEcho,
    NnIf,
    NnWhile,
    NnFunction,
    NnCall,
    NnReturn
)

class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self):
        self.pos += 1

    def expect(self, token_type):
        tok = self.peek()
        if tok and tok.type == token_type:
            self.advance()
            return tok
        raise SyntaxError(f'Мы думали, то что будет это {token_type}, а скрипт нам дал это {tok.type if tok else "EOF"}')

    def parse(self):
        if not (self.peek() and self.peek().type == 'НАЧ'):
            raise SyntaxError('Сунтах Ерор, не забывай, в начале скрипта ВСЕГДА должно быть НАЧ !')
        self.advance()
        statements = []
        while self.peek():
            statements.append(self.parse_statement())
        return NnProgram(statements)

    def parse_statement(self):
        tok = self.peek()
        if not tok:
            return None
        if tok.type == 'ID':
            return self.parse_assignment()
        elif tok.type == 'КРИКНИ':
            return self.parse_echo()
        elif tok.type == 'ЕСЛИ':
            return self.parse_if()
        elif tok.type == 'ДЕЛАЙ':
            return self.parse_while()
        elif tok.type == 'КУСОК':
            return self.parse_function()
        elif tok.type == 'ВЕРНУТЬ':
            return self.parse_return()
        else:
            return self.parse_expr()

    def parse_assignment(self):
        var_name = self.expect('ID').value
        self.expect('OP')
        expr = self.parse_expr()
        return NnAssign(var_name, expr)

    def parse_echo(self):
        self.expect('КРИКНИ')
        expr = self.parse_expr()
        return NnEcho(expr)

    def parse_if(self):
        self.expect('ЕСЛИ')
        self.expect('ЧЁ')
        condition = self.parse_expr()
        self.expect('ТО')
        then_body = self.parse_block()
        else_body = None
        if self.peek() and self.peek().type == 'НА':
            self.expect('НА')
            self.expect('ВСЯКИЙ')
            else_body = self.parse_block()
        return NnIf(condition, then_body, else_body)

    def parse_while(self):
        self.expect('ДЕЛАЙ')
        self.expect('ПОКА')
        condition = self.parse_expr()
        body = self.parse_block()
        return NnWhile(condition, body)

    def parse_function(self):
        self.expect('КУСОК')
        name = self.expect('ID').value
        self.expect('LPAREN')
        params = []
        if self.peek() and self.peek().type == 'ID':
            params.append(self.expect('ID').value)
            while self.peek() and self.peek().type == 'COMMA':
                self.expect('COMMA')
                params.append(self.expect('ID').value)
        self.expect('RPAREN')
        body = self.parse_block()
        return NnFunction(name, params, body)

    def parse_return(self):
        self.expect('ВЕРНУТЬ')
        expr = self.parse_expr()
        return NnReturn(expr)

    def parse_block(self):
        if self.peek() and self.peek().type == 'LBRACE':
            self.expect('LBRACE')
            statements = []
            while self.peek() and self.peek().type != 'RBRACE':
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
            self.expect('RBRACE')
            return statements
        else:
            return [self.parse_statement()]

    def parse_expr(self):
        return self.parse_or()

    def parse_or(self):
        left = self.parse_and()
        while self.peek() and self.peek().value == '||':
            self.expect('OP')
            right = self.parse_and()
            left = NnBinOp(left, '||', right)
        return left

    def parse_and(self):
        left = self.parse_equality()
        while self.peek() and self.peek().value == '&&':
            self.expect('OP')
            right = self.parse_equality()
            left = NnBinOp(left, '&&', right)
        return left

    def parse_equality(self):
        left = self.parse_comparison()
        while self.peek() and self.peek().value in ('==', '!='):
            op = self.expect('OP').value
            right = self.parse_comparison()
            left = NnBinOp(left, op, right)
        return left

    def parse_comparison(self):
        left = self.parse_term()
        while self.peek() and self.peek().value in ('<', '<=', '>', '>='):
            op = self.expect('OP').value
            right = self.parse_term()
            left = NnBinOp(left, op, right)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.peek() and self.peek().value in ('+', '-'):
            op = self.expect('OP').value
            right = self.parse_factor()
            left = NnBinOp(left, op, right)
        return left

    def parse_factor(self):
        left = self.parse_primary()
        while self.peek() and self.peek().value in ('*', '/'):
            op = self.expect('OP').value
            right = self.parse_primary()
            left = NnBinOp(left, op, right)
        return left

    def parse_primary(self):
        tok = self.peek()
        if not tok:
            raise SyntaxError("Неожиданный конец файла")
        if tok.type == 'NUMBER':
            self.advance()
            return NnNumber(tok.value)
        elif tok.type == 'STRING':
            self.advance()
            return NnString(tok.value)
        elif tok.type == 'СПРОСИКА':
            self.advance()
            if self.peek() and self.peek().type == 'LPAREN':
                self.expect('LPAREN')
                if self.peek() and self.peek().type == 'ID' and self.peek().value == 'число':
                    self.expect('ID')
                    self.expect('RPAREN')
                    return NnCall('input_number', [])
                else:
                    raise SyntaxError('СПРОСИКА поддерживает только (число)')
            return NnCall('input', [])
        elif tok.type == 'ID':
            name = self.expect('ID').value
            if self.peek() and self.peek().type == 'LPAREN':
                return self.parse_call(name)
            return NnVariable(name)
        elif tok.type == 'LPAREN':
            self.expect('LPAREN')
            expr = self.parse_expr()
            self.expect('RPAREN')
            return expr
        else:
            raise SyntaxError(f"Неожиданный токен: {tok.type}")

    def parse_call(self, name):
        self.expect('LPAREN')
        args = []
        if self.peek() and self.peek().type != 'RPAREN':
            args.append(self.parse_expr())
            while self.peek() and self.peek().type == 'COMMA':
                self.expect('COMMA')
                args.append(self.parse_expr())
        self.expect('RPAREN')
        return NnCall(name, args)
