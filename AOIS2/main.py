import itertools


def parse_expression(expr):
    # Замена символов логических операций на Python-совместимые
    replacements = {
        '&': ' and ',
        '|': ' or ',
        '!': ' not ',
        '->': ' <= ',  # Импликация
        '~': ' == '  # Эквиваленция
    }
    for old, new in replacements.items():
        expr = expr.replace(old, new)
    return expr


def truth_table(expr, variables):
    # Парсинг выражения для eval
    parsed_expr = parse_expression(expr)
    table = []
    # Генерация всех возможных комбинаций значений переменных
    for values in itertools.product([False, True], repeat=len(variables)):
        env = dict(zip(variables, values))
        # Вычисление результата выражения для текущей комбинации
        result = eval(parsed_expr, {}, env)
        table.append((values, result))
    return table


def sdnf_sknf(table, variables):
    sdnf = []
    sknf = []
    for values, result in table:
        if result:
            # Формирование конъюнкции для СДНФ
            term = [f"{var}" if val else f"!{var}" for var, val in zip(variables, values)]
            sdnf.append(f"({' & '.join(term)})")
        else:
            # Формирование дизъюнкции для СКНФ
            term = [f"!{var}" if val else f"{var}" for var, val in zip(variables, values)]
            sknf.append(f"({' | '.join(term)})")
    return ' | '.join(sdnf), ' & '.join(sknf)


def numeric_form(table, variables, form='sdnf'):
    indices = []
    for index, (values, result) in enumerate(table):
        # Определение индексов строк, соответствующих СДНФ или СКНФ
        if (form == 'sdnf' and result) or (form == 'sknf' and not result):
            indices.append(index)
    return indices


def index_form_binary(arr):
    binary_string = '0' * 8
    for index in arr:
        binary_string = binary_string[:index] + '1' + binary_string[index+1:]
    return binary_string

def index_form_decimal(binary_string):
    decimal = 0
    for i, digit in enumerate(binary_string):
        if digit == '1':
            decimal += 2 ** (len(binary_string) - i - 1)
    return decimal