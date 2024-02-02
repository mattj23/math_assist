
import sympy
from math_assist import Equation
from math_assist.output import Markdown


def main():
    x, y, z = sympy.symbols("x y z")
    eq = Equation(x**2 + 3, y*(y - 2) + 4)

    with Markdown(file_name="temp.md") as output:
        output("Original equation:")
        output(eq)


if __name__ == '__main__':
    main()