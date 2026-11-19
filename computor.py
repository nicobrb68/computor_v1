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


def get_degree(terms: dict[int, float]) -> int:
    non_zero_exps = [exp for exp, coeff in terms.items() if coeff != 0]
    return max(non_zero_exps) if non_zero_exps else 0

def ft_sqrt(n: float) -> float:
    if n <= 0:
        return 0.0
    guess = n
    for _ in range(30):
        guess = (guess + n / guess) / 2.0
    return guess

def solve(terms: dict[int, float], degree: int) -> None:
    if degree > 2:
        print("The polynomial degree is strictly greater than 2, I can't solve.")
        return

    c = terms.get(0, 0.0)
    b = terms.get(1, 0.0)
    a = terms.get(2, 0.0)

    if degree == 0:
        if c == 0:
            print("Any real number is a solution.")
        else:
            print("No solution.")
        return

    if degree == 1:
        sol = -c / b
        if sol == 0:
            sol = 0.0
        print("The solution is:")
        print(f"{sol:g}")
        return

    # Degree 2: compute discriminant (Delta = b^2 - 4ac)
    delta = b * b - 4 * a * c

    if delta > 0:
        sqrt_d = ft_sqrt(delta)
        x1 = (-b - sqrt_d) / (2 * a)
        x2 = (-b + sqrt_d) / (2 * a)
        print("Discriminant is strictly positive, the two solutions are:")
        print(f"{x1:g}")
        print(f"{x2:g}")
    elif delta == 0:
        x0 = -b / (2 * a)
        if x0 == 0:
            x0 = 0.0
        print("Discriminant is zero, the solution is:")
        print(f"{x0:g}")
    else:
        real = -b / (2 * a)
        imag = abs(ft_sqrt(-delta) / (2 * a))
        if real == 0:
            real = 0.0
        print("Discriminant is strictly negative, the two complex solutions are:")
        print(f"{real:g} + {imag:g}i")
        print(f"{real:g} - {imag:g}i")


if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            raw_equation = sys.argv[1]
        elif len(sys.argv) == 1:
            raw_equation = input()
        else:
            print("Usage: python3 computor.py \"<equation>\"")
            sys.exit(1)

        parsed_terms = parse_equation(raw_equation)
    except ValueError:
        print("Error: invalid equation format.")
        sys.exit(1)
    except (EOFError, KeyboardInterrupt):
        sys.exit(1)

    print(format_reduced_form(parsed_terms))
    degree = get_degree(parsed_terms)
    if degree > 0:
        print(f"Polynomial degree: {degree}")
    solve(parsed_terms, degree)