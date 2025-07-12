import re
from collections import namedtuple

Token = namedtuple('Token', ['type', 'value'])

KEYWORDS = {'КРИКНИ', 'НАЧ', 'ЕСЛИ', 'ЧЁ', 'ТО', 'НА', 'ВСЯКИЙ', 'ДЕЛАЙ', 'ПОКА', 'КУСОК', 'ВЕРНУТЬ', 'СПРОСИКА', 'ПОКРУТИ', 'ПРЫГНИ'}

TOKEN_SPECIFICATION = [
    ('NUMBER', r'\d+(\.\d*)?'),
    # Теперь поддержка русских и латинских букв в идентификаторах
    ('ID', r'[a-zA-Zа-яА-ЯёЁ_][a-zA-Zа-яА-ЯёЁ_0-9]*'),
    ('OP', r'[:]=|==|!=|<=|>=|[+\-*/=<>]'),
    ('SKIP', r'[ \t]+'),
    ('NEWLINE', r'\n'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('SEMICOLON', r';'),
    ('COMMA', r','),
    ('STRING', r'"[^"]*"'),
    ('MISMATCH', r'.'),
]


def lex(code):
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECIFICATION)

    for match in re.finditer(tok_regex, code):
        kind = match.lastgroup
        value = match.group()

        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
            yield Token(kind, value)
        elif kind == 'ID':
            # Проверяем составные ключевые слова
            if value.upper() in KEYWORDS:
                token_type = value.upper()
            else:
                token_type = 'ID'
            yield Token(token_type, value)
        elif kind == 'OP':
            yield Token(kind, value)
        elif kind == 'STRING':
            value = value[1:-1]
            yield Token(kind, value)
        elif kind in ('NEWLINE', 'SKIP'):
            continue
        elif kind in ('LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON', 'COMMA'):
            yield Token(kind, value)
        elif kind == 'MISMATCH':
            raise SyntaxError(f'Что-то неправильно: {value!r}')