
import sympy
from math_assist import Equation
from math_assist.output import Markdown


def main():
    x, y, z = sympy.symbols("x y z")
    eq = Equation(x**2 + 3, y*(y - 2) + 4)

    with Markdown(file_name="temp.md") as output:
        eq.attach_output(output)
        eq.multiply_by(2)
        eq.right.factor()
        eq.subtract(eq.right)
        eq.multiply_by(y*5 + 1)
        eq.expand()
        eq.swap_sides()
        eq.factor()
        eq.substitute(y, 3*x+1)




if __name__ == '__main__':
    main()