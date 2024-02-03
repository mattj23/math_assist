import sympy
from sympy import *
from math_assist import Equation, Expression
from math_assist.output import Markdown
from enum import Enum


class Side(Enum):
    INSIDE = 1
    OUTSIDE = 2


def xy_equations(arc0: Side):
    x, y, r0, s0, theta = symbols("x y r_0 s_0 theta")
    s_offset = r0 + s0 if arc0 is Side.OUTSIDE else r0 - s0
    x_eq = Equation(x, s_offset * cos(theta))
    y_eq = Equation(y, s_offset * sin(theta))
    return x, y, r0, s0, theta, x_eq, y_eq


def distance_equation(arc1: Side, x, y):
    s1, r1, h = symbols("s_1 r_1 h")
    dist = sqrt((h - x) ** 2 + y ** 2)
    if arc1 is Side.OUTSIDE:
        eq = Equation(s1, dist - r1)
    else:
        eq = Equation(s1, r1 - dist)
    return s1, r1, h, eq


def main():
    arc0 = Side.INSIDE
    arc1 = Side.INSIDE
    x, y, r0, s0, theta, x_eq, y_eq = xy_equations(arc0)
    s1, r1, h, eq = distance_equation(arc1, x=x, y=y)
    s = symbols("s")

    with Markdown(file_name="temp.md") as markdown:
        markdown("X and Y equations:")
        markdown(x_eq, y_eq)

        # Attach the main working equation
        eq.attach_output(markdown)

        # Isolate the root
        tree = eq.right.get_tree()
        sqrt_terms = tree.find_type(Pow)[0]
        route = sqrt_terms.route_from_root()
        for r in route:
            if r.node.func_type == sympy.Add:
                for c in r.other_children():
                    eq.subtract(c.item)
            elif r.node.func_type == sympy.Mul:
                for c in r.other_children():
                    eq.divide_by(c.item)
            else:
                raise ValueError(f"Unexpected type {r.node.func_type}")

        eq.substitute(x_eq)
        eq.substitute(y_eq)

        eq.to_power(2)
        eq.substitute(s1, s)
        eq.substitute(s0, s)
        eq.subtract_right()
        eq.left.expand()
        eq.left.collect([s, s ** 2])
        eq.left.simplify()
        # eq.left.collect([s])

        solutions = eq.solve(s)
        markdown("Solutions:")
        for sol in solutions:
            markdown(sol)

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
