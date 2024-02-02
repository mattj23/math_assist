from sympy import *
from math_assist import Equation, Expression
from math_assist.output import MarkdownOutput


def main():
    a_0, b_0, c_0, d_0, a_1, b_1, c_1, d_1 = symbols("a_0 b_0 c_0 d_0 a_1 b_1 c_1 d_1")
    theta, theta_0 = symbols("theta theta_0")
    lhs_n = a_0 * cos(theta) + b_0
    rhs_n = a_1 * cos(theta + theta_0) + b_1
    lhs_d = c_0 * cos(theta) + d_0
    rhs_d = c_1 * cos(theta + theta_0) + d_1

    eq = Equation(lhs_n / lhs_d, rhs_n / rhs_d)

    with MarkdownOutput(file_name="test.md") as markdown:
        markdown("Original equation:")
        markdown(eq)

        markdown("Multiply across by the denominators:")
        eq.multiply_by(lhs_d)
        eq.multiply_by(rhs_d)
        markdown(eq)

        markdown("Move across and expand:")
        eq.subtract(eq.right)
        eq.left.expand()
        markdown(eq)

        markdown("Move free terms to one side")
        free_terms = b_0 * d_1 - b_1 * d_0
        eq.subtract(free_terms)
        markdown(eq)

        markdown("Collect terms")
        terms = (cos(theta), cos(theta + theta_0), cos(theta) * cos(theta + theta_0))
        eq.left.collect(terms)
        markdown(eq)

        markdown("Divide by free terms")
        eq.divide_by(eq.right)
        eq.right.simplify()
        eq.left.expand()
        cfs = eq.left.collect(terms)
        markdown(eq)

        markdown("Prepare Substitutions:")
        a, b, c = symbols("a b c")
        for k, v in zip((a, b, c), cfs.values()):
            e = Equation(k, v)
            markdown(e)

            eq.left.substitute(e)

        markdown("Final Equation:")
        markdown(eq)


if __name__ == '__main__':
    main()
