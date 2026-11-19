import sys

def parse_equation(raw: str) -> dict[int, float]:
    cleaned = raw.replace(" ", "")
    left, right = cleaned.split("=")

    left_terms = [t for t in left.replace("-", "+-").split("+") if t]
    right_terms = [t for t in right.replace("-", "+-").split("+") if t]

    terms: dict[int, float] = {}

    for term in left_terms:
        if term == "0":
            continue
        coeff_str, exp_str = term.split("*X^")
        exp = int(exp_str)
        terms[exp] = terms.get(exp, 0.0) + float(coeff_str)

    for term in right_terms:
        if term == "0":
            continue
        coeff_str, exp_str = term.split("*X^")
        exp = int(exp_str)
        terms[exp] = terms.get(exp, 0.0) - float(coeff_str)

    return terms

def format_reduced_form(terms: dict[int, float]) -> str:
    if not terms or all(coeff == 0 for coeff in terms.values()):
        return "Reduced form: 0 * X^0 = 0"
    parts: list[str] = []
    for i, exp in enumerate(sorted(terms.keys())):
        coeff = terms[exp]
        if i == 0:
            parts.append(f"{coeff:g} * X^{exp}")
        elif coeff < 0:
            parts.append(f"- {abs(coeff):g} * X^{exp}")
        else:
            parts.append(f"+ {coeff:g} * X^{exp}")

    return f"Reduced form: {' '.join(parts)} = 0"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 computor.py \"<equation>\"")
        sys.exit(1)

    parsed_terms = parse_equation(sys.argv[1])
    print(format_reduced_form(parsed_terms))