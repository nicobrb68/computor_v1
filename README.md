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

## Features

- **Natural input parsing:** Supports standalone constants (`5`), omitted exponents (`4X`), implicit coefficients (`X^2`, `-X`), lowercase `x`, and unordered or duplicate terms.
- **Intermediate steps:** Displays extracted coefficients, discriminant evaluation, square root, and root formulas.
- **Irreducible fractions:** Formats rational real and complex solutions as simplified fractions (e.g., `-1/5 + 2i/5`).
- **Input validation:** Rejects invalid syntax, negative or fractional exponents (`X^-2`, `X^1.5`), consecutive operators (`++`, `+-`), missing operators (`5 2 * X`), and `nan`/`inf` values.
- **Clean reduced form:** Omits cancelled zero-coefficient terms while preserving `0 * X^0 = 0` when the full equation reduces to zero.

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