"""
    This module contains functions for plotting graphs and charts.
"""
from dataclasses import dataclass

import numpy
import sympy
from typing import Optional, Union, Tuple, List

from matplotlib.patches import FancyArrowPatch

from ._expression import Expression
from ._vector import VectorLike, as_np_vec, as_tuple_vec, rotate, normalized, distance, signed_angle_to
from matplotlib.pyplot import figure, Figure, Axes, close as close_figure


class AxesWrapper:
    def __init__(self, ax: Axes):
        self.ax: Axes = ax

        self._set_aspect_fill = False

    def equal_aspect(self, resize_subplot: bool = False):
        if resize_subplot:
            self.ax.set_aspect('equal')
        else:
            self._set_aspect_fill = True

    def _prepare(self):
        if self._set_aspect_fill:
            set_aspect_fill(self.ax)

    def plot(self, *args, **kwargs):
        if len(args) > 0 and isinstance(args[0], TraceBuilder):
            a0, *args = args
            self.ax.plot(*a0.args, *args, **kwargs)
        else:
            self.ax.plot(*args, **kwargs)

class PlotWrapper:
    def __init__(self, nrows: int = 1, ncols: int = 1, figsize: Tuple[int, int] = (6, 4), dpi: int = 300,
                 sharex: bool = False, sharey: bool = False, layout="tight"):
        self.fig = figure(figsize=figsize, dpi=dpi, layout=layout)
        self._subplots = self.fig.subplots(nrows, ncols, sharex=sharex, sharey=sharey, squeeze=False)
        self._wrapped = [[AxesWrapper(ax) for ax in row] for row in self._subplots]
        self._prepared = False

    def sp(self, row: int = 0, col: int = 0) -> AxesWrapper:
        return self._wrapped[row][col]

    def close(self):
        close_figure(self.fig)

    def _prepare_for_display(self):
        if not self._prepared:
            self._prepared = True
            for row in self._wrapped:
                for ax in row:
                    ax._prepare()

    def save(self, file_name: str, **kwargs):
        self._prepare_for_display()
        self.fig.savefig(file_name, **kwargs)

    def show(self, **kwargs):
        self._prepare_for_display()
        self.fig.show(**kwargs)


def plot_expression(ax: Axes, expr: Union[Expression, sympy.Expr]):
    """
    Plot a sympy expression on a given axis.

    :param ax: The axis to plot the expression on.
    :param expr: The expression to plot.
    """
    ex = expr if isinstance(expr, sympy.Expr) else expr.expr


def draw_arrow(ax: Axes,
               start: VectorLike,
               end: VectorLike,
               color: str = "black",
               arrow_style: str = "->",
               line_width: float = 0.75,
               line_style: str = "-",
               text: Optional[str] = None,
               text_position: float = 0.5,
               ha: str = "center",
               va: str = "center"):
    start = as_np_vec(start)
    end = as_np_vec(end)
    arrow = FancyArrowPatch(as_tuple_vec(start), as_tuple_vec(end), arrowstyle=arrow_style, mutation_scale=15,
                            color=color,
                            linewidth=line_width, linestyle=line_style)
    ax.add_patch(arrow)
    if text is not None:
        p = start + (end - start) * text_position
        draw_text(ax, p, text, ha=ha, va=va)


def dimension_with_leaders(ax: Axes,
                           start: VectorLike,
                           end: VectorLike,
                           offset: float,
                           direction: Optional[VectorLike] = None,
                           linewidth: float = 0.75,
                           linestyle: str = "-",
                           text: Optional[str] = None,
                           text_position: float = 0.5,
                           ha: str = "center",
                           va: str = "bottom",
                           v_nudge: float = 0.0):
    start = as_np_vec(start)
    end = as_np_vec(end)
    if direction is None:
        direction = normalized(end - start)
    else:
        direction = normalized(as_np_vec(direction))

    normal = rotate(direction, numpy.pi / 2)
    if offset < 0:
        normal *= -1
        offset = -offset

    x = normal.dot(end-start)
    if x > 0:
        d0 = abs(x)
        d1 = 0
    else:
        d0 = 0
        d1 = abs(x)

    p0 = start + normal * (offset + d0)
    p1 = end + normal * (offset + d1)
    l0 = FancyArrowPatch(as_tuple_vec(start), as_tuple_vec(p0),
                         arrowstyle="-", mutation_scale=15, color="black",
                         linewidth=linewidth, linestyle=linestyle)
    l1 = FancyArrowPatch(as_tuple_vec(end), as_tuple_vec(p1), arrowstyle="-", mutation_scale=30, color="black",
                         linewidth=linewidth, linestyle=linestyle)
    ax.add_patch(l0)
    ax.add_patch(l1)

    l2 = FancyArrowPatch(as_tuple_vec(p0), as_tuple_vec(p1), arrowstyle="<->", mutation_scale=15, color="black",
                         linewidth=linewidth, linestyle=linestyle)

    ax.add_patch(l2)

    if text is not None:
        p = p0 + (p1 - p0) * text_position
        draw_text(ax, p, text, ha=ha, va=va, v_nudge=v_nudge)


def draw_text(ax: Axes, position: VectorLike, text: str, ha: str = "center", va: str = "center", v_nudge: float = 0.0):
    position = as_np_vec(position)
    ax.annotate(text, (position[0], position[1] + v_nudge), ha=ha, va=va)


def set_aspect_fill(ax: Axes):
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()

    bbox = ax.get_window_extent()
    width, height = bbox.width, bbox.height

    x_scale = width / (x1 - x0)
    y_scale = height / (y1 - y0)

    if y_scale > x_scale:
        y_range = y_scale / x_scale * (y1 - y0)
        y_mid = (y0 + y1) / 2
        ax.set_ylim(y_mid - y_range / 2, y_mid + y_range / 2)
    else:
        x_range = x_scale / y_scale * (x1 - x0)
        x_mid = (x0 + x1) / 2
        ax.set_xlim(x_mid - x_range / 2, x_mid + x_range / 2)


@dataclass
class PlotBounds:
    x_min: float
    x_max: float
    y_min: float
    y_max: float

    def __post_init__(self):
        assert self.x_min <= self.x_max
        assert self.y_min <= self.y_max

    def set_x(self, ax: Axes):
        ax.set_xlim(self.x_min, self.x_max)

    def set_y(self, ax: Axes):
        ax.set_ylim(self.y_min, self.y_max)

    def set_xy(self, ax: Axes):
        self.set_x(ax)
        self.set_y(ax)

    def pad(self, padding: float):
        return PlotBounds(
            x_min=self.x_min - padding,
            x_max=self.x_max + padding,
            y_min=self.y_min - padding,
            y_max=self.y_max + padding,
        )

    def expand(self, fraction: float):
        x_mid = (self.x_min + self.x_max) / 2
        y_mid = (self.y_min + self.y_max) / 2
        x_range = (self.x_max - self.x_min) / 2
        y_range = (self.y_max - self.y_min) / 2
        return PlotBounds(
            x_min=x_mid - x_range * fraction,
            x_max=x_mid + x_range * fraction,
            y_min=y_mid - y_range * fraction,
            y_max=y_mid + y_range * fraction,
        )

    def __add__(self, other):
        return PlotBounds(
            x_min=min(self.x_min, other.x_min),
            x_max=max(self.x_max, other.x_max),
            y_min=min(self.y_min, other.y_min),
            y_max=max(self.y_max, other.y_max),
        )


class TraceBuilder:
    @staticmethod
    def line(start: VectorLike, end: VectorLike):
        return TraceBuilder(xs=[start[0], end[0]], ys=[start[1], end[1]])

    @staticmethod
    def arc(center: VectorLike, radius: float, start_angle: float, sweep_angle: float, points_per_degree: int = 1):
        n_points = int(abs(numpy.rad2deg(sweep_angle)) * points_per_degree)
        theta = numpy.linspace(0, sweep_angle, n_points) + start_angle
        x = center[0] + radius * numpy.cos(theta)
        y = center[1] + radius * numpy.sin(theta)
        return TraceBuilder(xs=x, ys=y)

    @staticmethod
    def arc_between(start: VectorLike, end: VectorLike, radius: float, clockwise=False, points_per_degree: int = 1):
        # To find the possible centers of the circle, we need to first find the possible intersections
        # between two circles of radius `radius` centered at `start` and `end`.  One of these will
        # be the center of the circle we want to draw.
        s = as_np_vec(start)
        e = as_np_vec(end)

        # We start by finding the vector from `start` to `end`, then with the starting point as a reference
        # we find the vc vector, which is halfway between the two circle centers. This forms one side of a
        # right triangle, whose hypotenuse is the radius and whose other side is the distance along the
        # perpendicular bisector.
        v = e - s
        vc = v / 2
        d = numpy.linalg.norm(vc)

        # We use the pythagorean theorem to find the distance along the perpendicular bisector
        # d^2 + b^2 = r^2
        b = numpy.sqrt(radius**2 - d**2)

        # We then find the unit vector along the perpendicular bisector, which is the vector from
        # start to end turned 90 degrees counter-clockwise and then normalized.
        u = normalized(rotate(v, numpy.pi/2))

        # To go in the clockwise direction, the center must be in the negative direction of the bisector,
        # otherwise it must be in the positive direction.
        c = s + vc + u * (-b if clockwise else b)

        v0 = s - c
        v1 = e - c
        sweep = signed_angle_to(v0, v1)
        if clockwise and sweep > 0:
            sweep -= 2 * numpy.pi
        elif not clockwise and sweep < 0:
            sweep += 2 * numpy.pi

        start_angle = signed_angle_to((1, 0), v0)
        return TraceBuilder.arc(c, radius, start_angle, sweep, points_per_degree)

    def __init__(self, xs: Optional[List[float]] = None, ys: Optional[List[float]] = None, c: Optional[List[float]] = None):
        self.xs = xs if xs is not None else []
        self.ys = ys if ys is not None else []
        self.c = c if c is not None else []

    def __add__(self, other):
        return TraceBuilder(
            xs=self.xs + other.xs,
            ys=self.ys + other.ys,
            c=self.c + other.c,
        )

    def bounds(self) -> PlotBounds:
        xs = [x for x in self.xs if x is not None]
        ys = [y for y in self.ys if y is not None]
        return PlotBounds(
            x_min=min(xs),
            x_max=max(xs),
            y_min=min(ys),
            y_max=max(ys),
        )

    def add_segment(self, *points: VectorLike):
        self.add_points(*points)
        self.add_blank()

    def add_blank(self):
        self.xs.append(None)
        self.ys.append(None)
        self.c.append(None)

    def add_points(self, *points: VectorLike):
        for x, y in points:
            self.xs.append(x)
            self.ys.append(y)

    def add_point_and_color(self, point: VectorLike, color: float):
        self.xs.append(point[0])
        self.ys.append(point[1])
        self.c.append(color)

    def invert_y(self):
        self.ys = [-y if y is not None else None for y in self.ys]

    @property
    def kwargs(self):
        return dict(x=self.xs, y=self.ys)

    @property
    def args(self):
        return self.xs, self.ys
