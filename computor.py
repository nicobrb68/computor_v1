import sys


def parse_term(term: str) -> tuple[float, int]:
    if term.startswith("*") or term.endswith("*") or term.count("*") > 1:
        raise ValueError("Invalid multiplication syntax")

    normalized = term.replace("x", "X")

    if "*" in normalized and "*X" not in normalized:
        raise ValueError("Operator '*' must precede 'X'")

    clean_term = normalized.replace("*", "")

    if "X" not in clean_term:
        coeff = float(clean_term)
        # nan check without math module
        if coeff != coeff or coeff in (float("inf"), float("-inf")):
            raise ValueError("Invalid numeric value")
        return coeff, 0

    if clean_term.count("X") != 1:
        raise ValueError("Multiple X in single term")

    coeff_part, exp_part = clean_term.split("X")

    # handle implicit 1 and -1 (e.g. "X^2", "-X")
    if coeff_part in ("", "+"):
        coeff = 1.0
    elif coeff_part == "-":
        coeff = -1.0
    else:
        coeff = float(coeff_part)
        if coeff != coeff or coeff in (float("inf"), float("-inf")):
            raise ValueError("Invalid coefficient")

    if exp_part == "":
        exp = 1
    elif exp_part.startswith("^") and exp_part[1:].isdigit():
        exp = int(exp_part[1:])
    else:
        raise ValueError("Invalid or negative exponent")

    return coeff, exp


def parse_equation(raw: str) -> dict[int, float]:
    if raw.count("=") != 1:
        raise ValueError("Invalid equation")

    # reject spaces between digits like "5 2 * X = 0"
    prev_char = ""
    saw_space = False
    for ch in raw:
        if ch.isspace():
            saw_space = True
        else:
            if saw_space and prev_char.isdigit() and ch.isdigit():
                raise ValueError("Missing operator between numbers")
            prev_char = ch
            saw_space = False

    cleaned = "".join(raw.split())

    for bad_seq in ("++", "--", "+-", "-+"):
        if bad_seq in cleaned:
            raise ValueError("Consecutive operators")

    left, right = cleaned.split("=")
    if not left or not right:
        raise ValueError("Empty side")

    left_terms = left.replace("-", "+-").split("+")
    right_terms = right.replace("-", "+-").split("+")

    # leading sign creates a single empty string at index 0
    if left_terms[0] == "":
        left_terms.pop(0)
    if right_terms[0] == "":
        right_terms.pop(0)

    if (
        not left_terms
        or not right_terms
        or "" in left_terms
        or "" in right_terms
    ):
        raise ValueError("Trailing or empty term")

    terms: dict[int, float] = {}

    # move everything to the left side (left - right = 0)
    for term in left_terms:
        coeff, exp = parse_term(term)
        terms[exp] = terms.get(exp, 0.0) + coeff

    for term in right_terms:
        coeff, exp = parse_term(term)
        terms[exp] = terms.get(exp, 0.0) - coeff

    return terms


def format_reduced_form(terms: dict[int, float]) -> str:
    non_zero_exps = sorted(exp for exp, coeff in terms.items() if coeff != 0)
    if not non_zero_exps:
        return "Reduced form: 0 * X^0 = 0"

    parts: list[str] = []
    for i, exp in enumerate(non_zero_exps):
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
    # babylonian method
    if n <= 0:
        return 0.0
    guess = n
    for _ in range(30):
        guess = (guess + n / guess) / 2.0
    return guess


def ft_gcd(a: int, b: int) -> int:
    # euclidean algorithm
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def format_fraction(num: float, den: float, imag: bool = False) -> str:
    # fallback to decimal for irrational roots
    num_str = f"{num:.10g}"
    den_str = f"{den:.10g}"
    if ("." in num_str and len(num_str.split(".")[1]) > 4) or (
        "." in den_str and len(den_str.split(".")[1]) > 4
    ):
        val = num / den
        if val == 0:
            val = 0.0
        return f"{abs(val):g}i" if imag else f"{val:g}"

    # scale exact decimals up to integers before reducing
    for _ in range(6):
        if num.is_integer() and den.is_integer():
            break
        num = round(num * 10, 6)
        den = round(den * 10, 6)

    n, d = int(round(num)), int(round(den))
    if n == 0:
        return "0i" if imag else "0"

    # keep minus sign on numerator
    if d < 0:
        n, d = -n, -d

    divisor = ft_gcd(n, d)
    n //= divisor
    d //= divisor

    if imag:
        n = abs(n)
        if d == 1:
            return "i" if n == 1 else f"{n}i"
        return f"{n}i/{d}"

    return f"{n}" if d == 1 else f"{n}/{d}"


def solve(terms: dict[int, float], degree: int) -> None:
    if degree > 2:
        print(
            "The polynomial degree is strictly greater than 2, "
            "I can't solve."
        )
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
        print(f"Step 1: Isolate X -> {b:g} * X = {-c:g}")
        print(f"Step 2: Divide by {b:g} -> X = {-c:g} / {b:g}")
        print("The solution is:")
        print(format_fraction(-c, b))
        return

    print(f"Step 1: Coefficients -> a = {a:g}, b = {b:g}, c = {c:g}")
    delta = b * b - 4 * a * c
    print(
        f"Step 2: Discriminant -> Delta = ({b:g})^2 "
        f"- 4 * ({a:g}) * ({c:g}) = {delta:g}"
    )

    if delta > 0:
        sqrt_d = ft_sqrt(delta)
        print(f"Step 3: Square root -> sqrt(Delta) = {sqrt_d:g}")
        print(
            f"Step 4: Roots -> x1 = ({-b:g} - {sqrt_d:g}) / (2 * {a:g}), "
            f"x2 = ({-b:g} + {sqrt_d:g}) / (2 * {a:g})"
        )
        print("Discriminant is strictly positive, the two solutions are:")
        print(format_fraction(-b - sqrt_d, 2 * a))
        print(format_fraction(-b + sqrt_d, 2 * a))
    elif delta == 0:
        print(f"Step 3: Single root -> x0 = {-b:g} / (2 * {a:g})")
        print("Discriminant is zero, the solution is:")
        print(format_fraction(-b, 2 * a))
    else:
        sqrt_d = ft_sqrt(-delta)
        real_str = format_fraction(-b, 2 * a)
        imag_str = format_fraction(sqrt_d, 2 * a, imag=True)
        print(
            f"Step 3: Square root of |Delta| -> "
            f"sqrt({-delta:g}) = {sqrt_d:g}"
        )
        print(
            f"Step 4: Complex split -> real = {-b:g} / (2 * {a:g}), "
            f"imag = {sqrt_d:g} / |(2 * {a:g})|"
        )
        print(
            "Discriminant is strictly negative, "
            "the two complex solutions are:"
        )
        print(f"{real_str} + {imag_str}")
        print(f"{real_str} - {imag_str}")


if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            raw_equation = sys.argv[1]
        elif len(sys.argv) == 1:
            raw_equation = input()
        else:
            print('Usage: python3 computor.py "<equation>"')
            sys.exit(1)

        parsed_terms = parse_equation(raw_equation)
    except ValueError as e:
        print(f"Error: {e}.")
        sys.exit(1)
    except (EOFError, KeyboardInterrupt):
        sys.exit(1)

    print(format_reduced_form(parsed_terms))
    degree = get_degree(parsed_terms)
    if degree > 0:
        print(f"Polynomial degree: {degree}")
    solve(parsed_terms, degree)
