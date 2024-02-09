import sympy
import numpy
from math_assist import Equation, Expression
from math_assist.output import Markdown
from matplotlib.pyplot import figure, Figure, Axes
from math_assist._plot import *
from math_assist._vector import *


def main():
    # f, u, v = sympy.symbols("f u v")
    # eq = Equation(1/f, 1/u + 1/v)
    #
    # with Markdown(file_name="temp.md") as md:
    #     eq.attach_output(md)
    #
    #     s = eq.solve(u)[0]
    #     md(s)
    #
    #     print(s.free_symbols)
    #
    #     sympy.plot(s)
    u = 10

    a0 = TraceBuilder.arc_between((0, -0.5), (0, 0.5), 5, clockwise=True)
    a1 = TraceBuilder.arc_between((0, 0.5), (0, -0.5), 5, clockwise=True)
    # a1 = TraceBuilder.arc_between((0, 0.5), (0, -0.5), 10, clockwise=True)

    plot = PlotWrapper(figsize=(8, 6))
    sp = plot.sp()
    sp.equal_aspect()
    sp.plot(a0, color="black", linewidth=1)
    sp.plot(a1, color="black", linewidth=1)
    dimension_with_leaders(sp.ax, (-1, 0), (0, -0.5), -0.25, direction=(1,0.1), text="$f$")
    plot.show()



if __name__ == '__main__':
    main()

