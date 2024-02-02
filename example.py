from sympy import *
from math_assist import Equation, Expression
from math_assist.output import Markdown


def main():
    x, y, r0, r1, s0, s1, theta, h, s = symbols("x y r_0 r_1 s_0 s_1 theta h s")
    x_eq = Equation(x, (r0 + s0) * cos(theta))
    y_eq = Equation(y, (r0 + s0) * sin(theta))
    eq = Equation(s1, sqrt((h-x)**2 + y**2) - r1)

    with Markdown(file_name="temp.md") as markdown:
        markdown("X and Y equations:")
        markdown(x_eq, y_eq)

        # Attach the main working equation
        eq.attach_output(markdown)

        eq.substitute(x_eq)
        eq.substitute(y_eq)
        eq.add(r1)
        eq.to_power(2)
        eq.substitute(s1, s)
        eq.substitute(s0, s)
        eq.subtract(eq.right)
        eq.left.expand()
        eq.left.collect([s, s**2])
        eq.left.simplify()
        eq.left.collect([s])

        # result = eq.solve(s).args[0]
        # sol = Equation(s, result)
        # markdown(sol)
        #
        # markdown("---")
        #
        # h1, h2, r2, theta_0 = symbols("h_1 h_2 r_2 theta_0")
        #
        # lhs = sol.right.clone()
        # rhs = sol.right.clone()
        #
        # lhs.substitute(h, h1)
        # rhs.substitute(h, h2)
        # rhs.substitute(r1, r2)
        # rhs.substitute(theta, theta + theta_0)
        #
        # _, d_rhs = rhs.as_fraction()
        # _, d_lhs = lhs.as_fraction()
        #
        # eq = Equation(lhs, rhs)
        # markdown("Intersection equation:")
        # markdown(eq)
        #
        # markdown("Multiply by denominators:")
        # eq.multiply_by(d_lhs)
        # eq.multiply_by(d_rhs)
        # eq.left.simplify()
        # eq.right.simplify()
        # markdown(eq)
        #
        # markdown("Move terms to left hand side:")
        # eq.subtract(eq.right)
        # markdown(eq)
        #
        # markdown("Expand left hand side:")
        # eq.left.expand()
        # markdown(eq)
        #
        # terms = [cos(theta), cos(theta + theta_0)]
        # markdown("Collect terms:")
        # cs = eq.left.collect(terms)
        # markdown(eq)
        #
        # markdown("Substitutions:")
        # a, b, c = symbols("a b c")
        # eq_a = Equation(cs[cos(theta)], a)
        # eq_b = Equation(cs[cos(theta + theta_0)], b)
        # eq_c = Equation(cs[1], c)
        # markdown(eq_a, eq_b, eq_c)
        #
        # eq.substitute(eq_a)
        # eq.substitute(eq_b)
        # eq.substitute(eq_c)
        # markdown(eq)
        #
        # # markdown("Solve for $\\theta$")
        # # # result = eq.solve(theta)
        # # result = solve(eq.eq, theta, domain=S.Reals)
        # # markdown(result)
        #
        # markdown("Acos")
        # eq.acos()
        # eq.left.simplify()
        # markdown(eq)





if __name__ == '__main__':
    main()
