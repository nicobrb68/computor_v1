# Computor v1

A Python command-line tool that reduces and solves polynomial equations up to degree 2, without using the `math` module or external libraries.

## Usage

With a command-line argument:

```bash
python3 computor.py "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"
```

With standard input (`stdin`):

```bash
echo "5 + 4 * X = 4" | python3 computor.py
```

## Solving Logic

Every equation is first simplified into its reduced form by moving all terms to the left-hand side:

$$aX^2 + bX + c = 0$$

- **Degree 0 ($c = 0$):** If $c = 0$, every real number is a solution. Otherwise, there is no solution.
- **Degree 1 ($bX + c = 0$):** Single solution $X = -\frac{c}{b}$.
- **Degree 2 ($aX^2 + bX + c = 0$):** Solved using the discriminant $\Delta = b^2 - 4ac$:

| Discriminant | Solutions | Formula |
| :--- | :--- | :--- |
| $\Delta > 0$ | 2 real solutions | $x_1 = \frac{-b - \sqrt{\Delta}}{2a}$, $x_2 = \frac{-b + \sqrt{\Delta}}{2a}$ |
| $\Delta = 0$ | 1 real solution | $x_0 = -\frac{b}{2a}$ |
| $\Delta < 0$ | 2 complex conjugate solutions | $x = -\frac{b}{2a} \pm \frac{\sqrt{-\Delta}}{2a}i$ |

- **Degree > 2:** Displays the polynomial degree and exits without solving.

## Implementation Details

### Square Root (`ft_sqrt`)
Implemented with the Babylonian (Heron's) method using only basic arithmetic:

$$x_{n+1} = \frac{1}{2}\left(x_n + \frac{N}{x_n}\right)$$

Running 30 iterations guarantees floating-point precision without relying on `math.sqrt`.

### Irreducible Fractions (`ft_gcd`)
Rational solutions are simplified using the Euclidean algorithm to compute the GCD:

```python
while b != 0:
    a, b = b, a % b
```

Exact decimal values are scaled to integers before reduction. Irrational roots (such as non-exact square roots) fall back to decimal notation.

## Bonus Features

### 1. Natural / Free-Form Input Parsing
Instead of requiring the strict `a * X^p` syntax on every term, the parser (`parse_term`) handles standard algebraic notation:
- Standalone constants without `* X^0` (e.g., `5` -> `5 * X^0`)
- Degree 1 terms without `^1` or `*` (e.g., `4X` or `4 * X` -> `4 * X^1`)
- Implicit `1` and `-1` coefficients (e.g., `X^2`, `-X`)
- Case-insensitive variable (`x` or `X`), unordered terms, and duplicate exponents on the same side

Example: `"5 + 4 * X + X^2 = X^2"` or `"-x + 3x^2 - 2 = 0"`.

### 2. Intermediate Resolution Steps
Before printing the final roots, `solve()` outputs each calculation step:
- **Degree 1:** Isolating `X` and dividing by its coefficient.
- **Degree 2:** Listing extracted coefficients (`a`, `b`, `c`), expanding $\Delta = b^2 - 4ac$, computing $\sqrt{\Delta}$ (or $\sqrt{|\Delta|}$), and showing the substituted root formula.

### 3. Irreducible Fractions
Both real and complex rational solutions are formatted as simplified fractions via `format_fraction()` and `ft_gcd()` instead of raw decimals:
- Scales exact decimals to integers, moves the minus sign to the numerator, and divides by the GCD.
- Simplifies denominators of `1` (e.g., `4/1` -> `4`, `1i` -> `i`) and formats complex fractions cleanly (e.g., `-1/5 + 2i/5`).
- Automatically falls back to decimal output when a square root is irrational.

### 4. Strict Syntax & Input Validation
Invalid inputs are caught early with explicit error messages instead of crashing or silently misparsing:
- Missing or multiple `=` signs, empty sides, and trailing operators (`5 * X^0 + = 0`)
- Consecutive operators (`++`, `--`, `+-`, `-+`)
- Negative or fractional exponents (`X^-2`, `X^1.5`)
- Missing operators between digits (`5 2 * X = 0`) and misplaced `*` (`5 * 2 * X = 0`)
- Non-finite floats (`nan`, `inf`) and invalid characters

### 5. Cleaned Reduced Form
`format_reduced_form()` filters out terms whose coefficients cancel out to `0` after reduction, keeping the output minimal while preserving `0 * X^0 = 0` when the entire equation reduces to zero.

Example: `"5 + 4 * X + X^2 = X^2"` outputs `Reduced form: 5 * X^0 + 4 * X^1 = 0` instead of keeping `+ 0 * X^2`.

## Examples

```bash
# Degree 2 (Delta > 0, irrational roots)
python3 computor.py "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"

# Degree 2 (Delta < 0, complex fractions)
python3 computor.py "1 * X^0 + 2 * X^1 + 5 * X^2 = 0"

# Degree 2 (Delta = 0)
python3 computor.py "1 * X^0 + 2 * X^1 + 1 * X^2 = 0"

# Natural form with X^2 cancellation (Degree 1)
python3 computor.py "5 + 4 * X + X^2 = X^2"

# Degree 3
python3 computor.py "8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0"
```