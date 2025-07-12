from core.lexer import lex
from core.parser import Parser
from core.ast import print_ast
from core.interpreter import run_interpreter

if __name__ == '__main__':
    try:
        code = open('script.nn', 'r', encoding='utf-8').read()
    except FileNotFoundError:
        print("Файл script.nn не найден! Создаю пример...")
        code = """НАЧ
x := 10
y := 20
КРИКНИ "Сумма: " + (x + y)

ЕСЛИ ЧЁ x > 5 ТО {
    КРИКНИ "x больше 5"
} НА ВСЯКИЙ {
    КРИКНИ "x меньше или равно 5"
}

ДЕЛАЙ ПОКА x > 0 {
    КРИКНИ x
    x := x - 1
}

КУСОК привет(имя) {
    КРИКНИ "Привет, " + имя
    ВЕРНУТЬ "Успешно"
}

результат := привет("Мир")
КРИКНИ "Результат функции: " + результат
"""

    tokens = list(lex(code))

    parser = Parser(tokens)
    ast = parser.parse()


    result = run_interpreter(ast)
    print(result)