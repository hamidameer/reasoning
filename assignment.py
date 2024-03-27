import re

def eliminate_implication(statement):
    statement = statement.replace("->" , "=>")

    a = statement.split("=>")
    p, q = a
    return f"(~{p})||({q})"


def demorgan(statement):
    return re.sub(r'~\((∀|∃)\s*\((.*?)\)\)', lambda m: '(' + ('∃' if m.group(1) == '∀' else '∀') + '~' + m.group(2) + ')', statement)


def double_not(statement):
    return re.sub(r'~~(\w+)', r'\1', statement)


def standardize_scope(statement):
    v_map = {}
    v_pattern = re.compile(r'[∀∃]\((\w+)\)')
    count = 1
    def replace_variable(match):
        
        nonlocal count
        variable = match.group(1)

        if variable not in v_map:
            standardized_variable = f'v{count}'
            count += 1
            v_map[variable] = standardized_variable

        return variable_map[variable]

    return re.sub(v_pattern, replace_variable, statement)


def prenex_form(statement):
    q, m = re.match(r'((∀|∃)*)(.*)', statement).group(1, 3)
    
    return q + standardize_scope(m)



def eliminate_universal(statement):
    
    return re.sub(r'∀([a-zA-Z]\w*):', '', statement)


def to_cnf(statement):
    statement = eliminate_implication(statement)
    statement = demorgan(statement)
    statement = double_not(statement)
    statement = standardize_scope(statement)
    statement = prenex_form(statement)
    statement = eliminate_universal(statement)

    
    return statement


def distribute_disjunction(l, r):
    l_terms = l.split("&&")
    r_terms = r.split("&&")
    distributed_terms = []
    for l_term in l_terms:
        for r_term in r_terms:
            distributed_terms.append(f"({l_term} || {r_term})")
    return " && ".join(distributed_terms)


statement = "~(∀(P -> ∃x Q(x)))"
print("statement:", statement)

cnf = to_cnf(statement)
print("After Conversion to CNF:", cnf)
