"""
    This is an example of working with expressions using the math_assist library.

"""

import sympy
from math_assist import Expression
from math_assist.output import Markdown


def main():
    x = sympy.symbols("x")

    with Markdown(file_name="temp.md") as output:
        # Create an expression
        output("Initial expression:")
        expr = Expression(x**2 + 2*x + 1)
        output(expr)

        # Factor the expression
        output("Factored expression:")
        expr.apply(sympy.factor)
        output(expr)

        # Add a step to the history
        output("Added x^3 + 2:")
        expr.add(x**3 + 2)
        output(expr)

        # Expand the expression
        output("Expanded expression:")
        expr.expand()
        output(expr)

        # Factor the expression
        output("Factored expression:")
        expr.factor()
        output(expr)

        output("---")

        expr.history.write_all_to(output)


if __name__ == "__main__":
    main()