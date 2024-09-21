import itertools

def replace_operators(logical_expression):
    operator_mapping = {
        '!': ' not ',
        '&': ' and ',
        '|': ' or ',
        '->': ' <= ',
        '~': ' == ',
    }
    for old_op, new_op in operator_mapping.items():
        logical_expression = logical_expression.replace(old_op, new_op)
    return logical_expression
def evaluate_expression(expr, vars_values):
    # Создаем словарь для сопоставления переменных с их значениями
    defaults = {'a': False, 'b': False, 'c': False, 'd': False, 'e': False}
    # Заполняем словарь значениями из vars_values
    for i, var in enumerate(vars_values):
        defaults[list(defaults.keys())[i]] = var
    # Заменяем операторы в выражении
    modified_expr = replace_operators(expr)
    # Используем локальные переменные для дальнейших вычислений
    a, b, c, d, e = defaults['a'], defaults['b'], defaults['c'], defaults['d'], defaults['e']
    # Выполняем выражение с eval
    return eval(modified_expr)


def truth_table(logical_expression, variables='abcde'):
    # Определяем количество переменных, присутствующих в выражении
    active_vars = len([var for var in variables if var in logical_expression])
    # Генерируем все комбинации значений переменных (0 и 1) для активных переменных
    all_combinations = []
    for i in range(2 ** active_vars):  # Генерация через бинарные числа
        combination = tuple(int(bit) for bit in f'{i:0{active_vars}b}')
        all_combinations.append(combination)
    # Обрабатываем логическое выражение и заменяем операторы
    transformed_expression = replace_operators(logical_expression)
    # Вычисляем результат для каждой комбинации
    results = []
    for combination in all_combinations:
        results.append(evaluate_expression(transformed_expression, combination))
    # Возвращаем количество активных переменных и результаты
    return active_vars, list(zip(all_combinations, results))

def build_sdnf_cnf_forms(rows, active_vars, variables='abcde'):
    sdnf_terms = []
    cnf_terms = []
    # Разделение строк на те, где результат True и False
    for combination, result in rows:
        if result:
            sdnf_terms.append(combination)
        else:
            cnf_terms.append(combination)
    # Построение СДНФ через поэтапный цикл, вместо одного вложенного выражения
    sdnf_parts = []
    for combination in sdnf_terms:
        term = []
        for var, bit in zip(variables[:active_vars], combination):
            term.append(f'{var}' if bit else f'!{var}')
        sdnf_parts.append(' & '.join(term))
    sdnf_expression = ' | '.join(sdnf_parts)
    # Построение СКНФ также по шагам
    cnf_parts = []
    for combination in cnf_terms:
        clause = []
        for var, bit in zip(variables[:active_vars], combination):
            clause.append(f'{var}' if bit else f'!{var}')
        cnf_parts.append(f"({' | '.join(clause)})")
    cnf_expression = ' & '.join(cnf_parts)
    return sdnf_expression, cnf_expression


def merge_terms(term1, term2):
    differences = 0
    result_term = list(term1)  # Копируем первый терм для изменения
    # Проходим по обеим термам, сравнивая их элементы
    for index in range(len(term1)):
        if term1[index] != term2[index]:
            result_term[index] = '-'  # Если элементы различаются, заменяем на '-'
            differences += 1
        # Если одинаковы, оставляем исходное значение из term1 (это уже сделано)

    # Возвращаем терм, только если ровно одно различие
    if differences == 1:
        return result_term
    return None


def find_implicants(minterms):
    prime_implicants = set()  # Множество для хранения простых импликант
    while len(minterms) > 0:
        merged_terms = []  # Список для хранения новых термов после слияния
        used_terms = set()  # Множество для отслеживания использованных термов
        # Сравниваем все термы
        for i in range(len(minterms)):
            term1 = minterms[i]
            for j in range(i + 1, len(minterms)):
                term2 = minterms[j]
                merged_term = merge_terms(term1, term2)
                if merged_term is not None:
                    print(f"Merging terms: {term1} and {term2} -> {merged_term}")
                    merged_terms.append(merged_term)
                    used_terms.add(tuple(term1))  # Отмечаем использованный терм
                    used_terms.add(tuple(term2))
        # Определяем термы, которые не были использованы
        unused_terms = set(map(tuple, minterms)) - used_terms
        prime_implicants.update(unused_terms)
        # Переходим к новым термам для следующей итерации
        minterms = merged_terms
    return prime_implicants


def identify_essential_implicants(implicants, minterms):
    essential_implicants = set()
    for minterm in minterms:
        unique_implicant = None
        for imp in implicants:
            if all((bit == '-' or bit == t_bit) for bit, t_bit in zip(imp, minterm)):
                if unique_implicant is not None:
                    unique_implicant = None  # Найдено больше одного импликанта
                    break
                unique_implicant = imp  # Запоминаем единственный импликант
        if unique_implicant is not None:
            essential_implicants.add(unique_implicant)
    return essential_implicants


def minimize_using_qm(entries, active_vars, is_sdnf=True):
    # Фильтруем минтермы на основе типа логической функции
    minterms = filter(lambda entry: entry[1] == is_sdnf, entries)
    minterms = [entry[0] for entry in minterms]
    print(f"\nInitial minterms {'SDNF' if is_sdnf else 'CNF'}: {minterms}")
    # Получаем простые импликанты
    prime_implicants = find_implicants(minterms)
    print(f"Prime Implicants: {prime_implicants}")
    # Создаем множество essential импликантов
    essential_implicants = set()
    minterm_coverage = {term: 0 for term in minterms}
    for implicant in prime_implicants:
        for term in minterms:
            if all((bit == '-' or bit == t_bit) for bit, t_bit in zip(implicant, term)):
                minterm_coverage[term] += 1
    for term in minterms:
        if minterm_coverage[term] == 1:
            essential_implicants.add(term)
    # Определяем оставшиеся минтермы
    remaining_minterms = []
    for term in minterms:
        if not any(
            all((bit == '-' or bit == t_bit) for bit, t_bit in zip(implicant, term))
            for implicant in essential_implicants):
                remaining_minterms.append(term)
    return essential_implicants, remaining_minterms

def format_result(implicant, active_vars, variables='abcde', is_sdnf=True):
    # Определяем логическую операцию на основе is_sdnf
    logic_op = ' & ' if is_sdnf else ' | '
    formatted_terms = []
    for var, bit in zip(variables[:active_vars], implicant):
        if bit != '-':
            if (bit == 1 and is_sdnf) or (bit == 0 and not is_sdnf):
                formatted_terms.append(var)
            else:
                formatted_terms.append(f'!{var}')
    formatted_implicant = logic_op.join(formatted_terms)
    return formatted_implicant


def generate_implicant_chart(implicants, minterms):
    chart = {}
    for minterm in minterms:
        matching_implicants = []
        for imp in implicants:
            if all((bit == '-' or bit == t_bit) for bit, t_bit in zip(imp, minterm)):
                matching_implicants.append(imp)
        chart[tuple(minterm)] = matching_implicants
    return chart

def quine_mccluskey_with_chart_display(entries, active_vars, is_sdnf=True):
    # Фильтруем минтермы по типу логической функции
    minterms = [entry[0] for entry in entries if entry[1] == is_sdnf]
    print(f"\nInitial minterms {'SDNF' if is_sdnf else 'CNF'}: {minterms}")
    # Находим простые импликанты
    prime_implicants = find_implicants(minterms)
    print(f"Prime Implicants: {prime_implicants}")

    # Определяем essential импликанты
    essential_implicants = set()
    for term in minterms:
        covered = [imp for imp in prime_implicants if
                   all((bit == '-' or bit == t_bit) for bit, t_bit in zip(imp, term))]
        if len(covered) == 1:
            essential_implicants.add(covered[0])

    # Определяем оставшиеся минтермы
    remaining_minterms = []
    for term in minterms:
        if not any(
                all((bit == '-' or bit == t_bit) for bit, t_bit in zip(imp, term))
                for imp in essential_implicants):
            remaining_minterms.append(term)
    # Генерируем таблицу импликантов
    chart = generate_implicant_chart(prime_implicants, remaining_minterms)
    return essential_implicants, remaining_minterms, chart


def binary_to_decimal(binary_values):
    return int(''.join(str(bit) for bit in binary_values), 2)


def generate_kmap(entries, active_vars, is_sdnf=True):
    # Определяем размер карты Карно
    half_vars = (active_vars + 1) // 2
    map_size = 2 ** half_vars
    kmap = [[0 for _ in range(map_size)] for _ in range(map_size)]  # Инициализируем карту нулями
    for combination, result in entries:
        mark_cell = (result and is_sdnf) or (not result and not is_sdnf)
        if mark_cell:
            mid_index = len(combination) // 2
            row_bits = combination[:mid_index]
            col_bits = combination[mid_index:]
            row = binary_to_decimal(row_bits)
            col = binary_to_decimal(col_bits)
            kmap[row][col] = 1  # Устанавливаем значение ячейки в 1
    return kmap

def expression_to_dnf(expr):
    # Заменяем операторы
    transformed_expr = replace_operators(expr)
    # Строим таблицу истинности
    active_vars, truth_entries = truth_table(transformed_expr)
    # Формируем ДНФ
    dnf_parts = []
    for combination, result in truth_entries:
        if result:
            term = []
            for var, bit in zip('abcde'[:active_vars], combination):
                term.append(f'{var}' if bit else f'!{var}')
            dnf_parts.append('(' + ' & '.join(term) + ')')
    dnf_expression = ' | '.join(dnf_parts)
    return dnf_expression

def expression_to_cnf(expr):
    # Заменяем операторы
    transformed_expr = replace_operators(expr)
    # Строим таблицу истинности
    active_vars, truth_entries = truth_table(transformed_expr)
    # Формируем КНФ
    cnf_parts = []
    for combination, result in truth_entries:
        if not result:
            clause = []
            for var, bit in zip('abcde'[:active_vars], combination):
                clause.append(f'!{var}' if bit else f'{var}')
            cnf_parts.append(f"({' | '.join(clause)})")
    cnf_expression = ' & '.join(cnf_parts)
    return cnf_expression

def print_normal_forms(expr):
    dnf = expression_to_dnf(expr)
    cnf = expression_to_cnf(expr)
    print(f"\nDNF of {expr}: {dnf}")
    print(f"CNF of {expr}: {cnf}")



def analyze_variable_usage(logical_expression):
    # Инициализируем словарь для подсчета использования переменных
    variable_count = {var: 0 for var in 'abcde'}

    # Считаем вхождения переменных
    for char in logical_expression:
        if char in variable_count:
            variable_count[char] += 1

    # Фильтруем переменные, которые не использовались
    used_variables = {var: count for var, count in variable_count.items() if count > 0}
    return used_variables

