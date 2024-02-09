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


def work_out_rlfs(arc0: Side, arc1: Side, output: Markdown):
    x, y, r0, s0, theta, x_eq, y_eq = xy_equations(arc0)
    s1, r1, h, eq = distance_equation(arc1, x=x, y=y)
    s = symbols("s")

    output("X and Y equations:")
    output(x_eq, y_eq)
    eq.attach_output(output)

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
    solutions = eq.solve(s)
    assert len(solutions) == 1
    sol = solutions[0]
    output("Solution:")
    output(sol)

    eq.detach_all_outputs()

    return Expression(sol)

def to_simplified_coeffs(lhs: Expression, rhs: Expression, md: Markdown):
    h, r1, theta, h1, h2, r2, theta_0 = symbols("h r1 theta h_1 h_2 r_2 theta_0")
    lhs.substitute(h, h1)
    rhs.substitute(h, h2)
    rhs.substitute(r1, r2)
    rhs.substitute(theta, theta + theta_0)

    eq = Equation(lhs, rhs)
    eq.attach_output(md)

    n_lhs, d_lhs = eq.left.as_fraction()
    n_rhs, d_rhs = eq.right.as_fraction()
    eq.multiply_by(d_lhs * d_rhs)
    eq.subtract_right()
    eq.left.simplify()
    eq.left.expand()
    terms = [cos(theta), cos(theta + theta_0)]
    eq.left.collect(terms)
    cs = eq.left.collect_coeffs_only(terms)

    md("Substitutions:")
    a, b, c = symbols("a b c")
    eq_a = Equation(cs[cos(theta)], a)
    eq_b = Equation(cs[cos(theta + theta_0)], b)
    eq_c = Equation(cs[1], c)
    md(eq_a, eq_b, eq_c)

    eq.substitute(eq_a)
    eq.substitute(eq_b)
    eq.substitute(eq_c)


def main():
    with Markdown(file_name="temp.md") as md:
        md("# Derivations for RLFS of Two Arcs")

        md("## Inside Facing Arc")
        md("### Inside Facing to Outside Facing")
        in_out = work_out_rlfs(Side.INSIDE, Side.OUTSIDE, md)

        md("### Inside Facing to Inside Facing")
        in_in = work_out_rlfs(Side.INSIDE, Side.INSIDE, md)

        md("### Intersections Between RLFS of Two Arcs")

        md("**Second Arcs are Both Outside Facing**\n")
        to_simplified_coeffs(in_out.clone(), in_out.clone(), md)

        md("**Second Arcs are Both Inside Facing**\n")
        to_simplified_coeffs(in_in.clone(), in_in.clone(), md)

        md("**Second Arcs are One Inside and One Outside Facing**\n")
        to_simplified_coeffs(in_out.clone(), in_in.clone(), md)

        md("## Outside Facing Arc")
        md("### Outside Facing to Outside Facing")
        out_out = work_out_rlfs(Side.OUTSIDE, Side.OUTSIDE, md)

        md("### Outside Facing to Inside Facing")
        out_in = work_out_rlfs(Side.OUTSIDE, Side.INSIDE, md)

        md("### Intersections Between RLFS of Two Arcs")

        md("**Second Arcs are Both Outside Facing**\n")
        to_simplified_coeffs(out_out.clone(), out_out.clone(), md)

        md("**Second Arcs are Both Inside Facing**\n")
        to_simplified_coeffs(out_in.clone(), out_in.clone(), md)

        md("**Second Arcs are One Inside and One Outside Facing**\n")
        to_simplified_coeffs(out_out.clone(), out_in.clone(), md)



if __name__ == '__main__':
    main()
