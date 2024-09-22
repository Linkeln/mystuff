def merge_terms(term1, term2):
    differences = 0
    result_term = list(term1)
    for index in range(len(term1)):
        if term1[index] != term2[index]:
            result_term[index] = '-'
            differences += 1
    if differences == 1:
        return result_term
    return None

def find_implicants(minterms):
    prime_implicants = set()
    while minterms:
        merged_terms = []
        used_terms = set()
        for i in range(len(minterms)):
            term1 = minterms[i]
            for j in range(i + 1, len(minterms)):
                term2 = minterms[j]
                merged_term = merge_terms(term1, term2)
                if merged_term:
                    merged_terms.append(merged_term)
                    used_terms.update({tuple(term1), tuple(term2)})
        unused_terms = set(map(tuple, minterms)) - used_terms
        prime_implicants.update(unused_terms)
        minterms = merged_terms
    return prime_implicants

def quine_mccluskey_with_chart_display(entries, active_vars, is_sdnf=True):
    minterms = [entry[0] for entry in entries if entry[1] == is_sdnf]
    prime_implicants = find_implicants(minterms)
    essential_implicants = set()
    for term in minterms:
        covered = [imp for imp in prime_implicants if
                   all((bit == '-' or bit == t_bit) for bit, t_bit in zip(imp, term))]
        if len(covered) == 1:
            essential_implicants.add(covered[0])
    remaining_minterms = []
    for term in minterms:
        if not any(
                all((bit == '-' or bit == t_bit) for bit, t_bit in zip(imp, term))
                for imp in essential_implicants):
            remaining_minterms.append(term)
    chart = generate_implicant_chart(prime_implicants, remaining_minterms)
    return essential_implicants, remaining_minterms, chart

def generate_implicant_chart(implicants, minterms):
    chart = {}
    for minterm in minterms:
        matching_implicants = []
        for imp in implicants:
            if all((bit == '-' or bit == t_bit) for bit, t_bit in zip(imp, minterm)):
                matching_implicants.append(imp)
        chart[tuple(minterm)] = matching_implicants
    return chart

def display_implicant_chart(chart):
    for minterm, implicants in chart.items():
        minterm_str = ''.join(str(bit) for bit in minterm)
        implicants_str = ', '.join(''.join(imp) for imp in implicants)
        print(f"{minterm_str}: {implicants_str}")
    print()
    return True

def display_minimized_result(essential_implicants, active_vars, variables='ABCD', is_sdnf=True):
    if not essential_implicants:
        print("No essential implicants found.")
        return

    formatted_implicants = []
    for implicant in essential_implicants:
        formatted_implicants.append(format_result(implicant, active_vars, variables, is_sdnf))

    logic_op = ' | ' if is_sdnf else ' & '
    minimized_expression = logic_op.join(formatted_implicants)

    print(f"\nMinimized {'SDNF' if is_sdnf else 'CNF'} result:")
    print(minimized_expression)
    return True

def format_result(implicant, active_vars, variables='ABCD', is_sdnf=True):
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

def laba_4_1():
    # Example input: list of tuples (minterm, result), where result is True for SDNF and False for CNF
    # Assuming a logical expression with 3 variables: a, b, c
    entries = [
        ((0, 0, 0, 0), False),
        ((0, 0, 0, 1), False),
        ((0, 0, 1, 0), False),
        ((0, 0, 1, 1), False),
        ((0, 1, 0, 0), True),
        ((0, 1, 0, 1), True),
        ((0, 1, 1, 0), True),
        ((0, 1, 1, 1), True),
        ((1, 0, 0, 0), True),
        ((1, 0, 0, 1), True)
    ]
    active_vars = 4  # Number of active variables in the expression

    # Perform minimization using the Quine-McCluskey method for SDNF
    essential_implicants, remaining_minterms, chart = quine_mccluskey_with_chart_display(entries, active_vars, is_sdnf=True)

    # Display the minimized result
    display_minimized_result(essential_implicants, active_vars, is_sdnf=True)

    # Display the implicant chart
    display_implicant_chart(chart)

    entries = [
        ((0, 0, 0, 0), True),
        ((0, 0, 0, 1), True),
        ((0, 0, 1, 0), True),
        ((0, 0, 1, 1), True),
        ((0, 1, 0, 0), False),
        ((0, 1, 0, 1), False),
        ((0, 1, 1, 0), False),
        ((0, 1, 1, 1), False),
        ((1, 0, 0, 0), True),
        ((1, 0, 0, 1), True)
    ]
    active_vars = 4  # Number of active variables in the expression

    # Perform minimization using the Quine-McCluskey method for SDNF
    essential_implicants, remaining_minterms, chart = quine_mccluskey_with_chart_display(entries, active_vars, is_sdnf=True)

    # Display the minimized result
    display_minimized_result(essential_implicants, active_vars, is_sdnf=True)

    # Display the implicant chart
    display_implicant_chart(chart)


    entries = [
        ((0, 0, 0, 0), False),
        ((0, 0, 0, 1), False),
        ((0, 0, 1, 0), True),
        ((0, 0, 1, 1), True),
        ((0, 1, 0, 0), False),
        ((0, 1, 0, 1), False),
        ((0, 1, 1, 0), True),
        ((0, 1, 1, 1), True),
        ((1, 0, 0, 0), False),
        ((1, 0, 0, 1), False)
    ]
    active_vars = 4  # Number of active variables in the expression

    # Perform minimization using the Quine-McCluskey method for SDNF
    essential_implicants, remaining_minterms, chart = quine_mccluskey_with_chart_display(entries, active_vars, is_sdnf=True)

    # Display the minimized result
    display_minimized_result(essential_implicants, active_vars, is_sdnf=True)

    # Display the implicant chart
    display_implicant_chart(chart)

    entries = [
        ((0, 0, 0, 0), False),
        ((0, 0, 0, 1), True),
        ((0, 0, 1, 0), False),
        ((0, 0, 1, 1), True),
        ((0, 1, 0, 0), False),
        ((0, 1, 0, 1), True),
        ((0, 1, 1, 0), False),
        ((0, 1, 1, 1), True),
        ((1, 0, 0, 0), False),
        ((1, 0, 0, 1), True)
    ]
    active_vars = 4  # Number of active variables in the expression

    # Perform minimization using the Quine-McCluskey method for SDNF
    essential_implicants, remaining_minterms, chart = quine_mccluskey_with_chart_display(entries, active_vars, is_sdnf=True)

    # Display the minimized result
    display_minimized_result(essential_implicants, active_vars, is_sdnf=True)

    # Display the implicant chart
    display_implicant_chart(chart)



def laba_4_2():
    entries = [
        ((0, 0, 0), False),
        ((0, 0, 1), True),
        ((0, 1, 0), True),
        ((0, 1, 1), False),
        ((1, 0, 0), True),
        ((1, 0, 1), False),
        ((1, 1, 0), False),
        ((1, 1, 1), True)
    ]
    active_vars = 3  # Number of active variables in the expression

    # Perform minimization using the Quine-McCluskey method for SDNF
    essential_implicants, remaining_minterms, chart = quine_mccluskey_with_chart_display(entries, active_vars, is_sdnf=True)

    # Display the minimized result
    display_minimized_result(essential_implicants, active_vars, is_sdnf=True)

    # Display the implicant chart
    display_implicant_chart(chart)

    entries = [
        ((0, 0, 0), False),
        ((0, 0, 1), False),
        ((0, 1, 0), False),
        ((0, 1, 1), True),
        ((1, 0, 0), False),
        ((1, 0, 1), True),
        ((1, 1, 0), True),
        ((1, 1, 1), True)
    ]
    active_vars = 3  # Number of active variables in the expression

    # Perform minimization using the Quine-McCluskey method for SDNF
    essential_implicants, remaining_minterms, chart = quine_mccluskey_with_chart_display(entries, active_vars, is_sdnf=True)

    # Display the minimized result
    display_minimized_result(essential_implicants, active_vars, is_sdnf=True)

    # Display the implicant chart
    display_implicant_chart(chart)

def laba_5():
    entries = [
        ((0, 0, 0), True),
        ((0, 0, 1), False),
        ((0, 1, 0), True),
        ((0, 1, 1), False),
        ((1, 0, 0), True),
        ((1, 0, 1), False),
        ((1, 1, 0), True),
        ((1, 1, 1), False)
    ]
    active_vars = 3  # Number of active variables in the expression

    # Perform minimization using the Quine-McCluskey method for SDNF
    essential_implicants, remaining_minterms, chart = quine_mccluskey_with_chart_display(entries, active_vars, is_sdnf=True)

    # Display the minimized result
    display_minimized_result(essential_implicants, active_vars, is_sdnf=True)

    # Display the implicant chart
    display_implicant_chart(chart)

    entries = [
        ((0, 0, 0), False),
        ((0, 0, 1), True),
        ((0, 1, 0), True),
        ((0, 1, 1), False),
        ((1, 0, 0), False),
        ((1, 0, 1), True),
        ((1, 1, 0), True),
        ((1, 1, 1), False)
    ]
    active_vars = 3  # Number of active variables in the expression

    # Perform minimization using the Quine-McCluskey method for SDNF
    essential_implicants, remaining_minterms, chart = quine_mccluskey_with_chart_display(entries, active_vars, is_sdnf=True)

    # Display the minimized result
    display_minimized_result(essential_implicants, active_vars, is_sdnf=True)

    # Display the implicant chart
    display_implicant_chart(chart)

    entries = [
        ((0, 0, 0), False),
        ((0, 0, 1), False),
        ((0, 1, 0), False),
        ((0, 1, 1), True),
        ((1, 0, 0), True),
        ((1, 0, 1), True),
        ((1, 1, 0), True),
        ((1, 1, 1), False)
    ]
    active_vars = 3  # Number of active variables in the expression

    # Perform minimization using the Quine-McCluskey method for SDNF
    essential_implicants, remaining_minterms, chart = quine_mccluskey_with_chart_display(entries, active_vars, is_sdnf=True)

    # Display the minimized result
    display_minimized_result(essential_implicants, active_vars, is_sdnf=True)

    # Display the implicant chart
    display_implicant_chart(chart)
# Run the example
laba_5()