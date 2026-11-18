import sys

def parse_equation(raw: str) -> dict[int, float]:
    cleaned = raw.replace(" ", "")
    left, right = cleaned.split("=")

    left_terms = [t for t in left.replace("-", "+-").split("+") if t]
    right_terms = [t for t in right.replace("-", "+-").split("+") if t]

    terms: dict[int, float] = {}

    for term in left_terms:
        coeff_str, exp_str = term.split("*X^")
        exp = int(exp_str)
        terms[exp] = terms.get(exp, 0.0) + float(coeff_str)

    for term in right_terms:
        coeff_str, exp_str = term.split("*X^")
        exp = int()