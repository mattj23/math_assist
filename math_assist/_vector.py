"""
    This module has tools for working with numpy arrays of form [float, float] as if they were
    vectors.  This is mostly used for plotting.
"""

import numpy
from typing import Union, Tuple, List

VectorLike = Union[Tuple[float, float], List[float], numpy.ndarray]


def as_np_vec(v: VectorLike) -> numpy.ndarray:
    if isinstance(v, numpy.ndarray):
        # Check to make sure the shape is correct
        return v
    elif isinstance(v, list):
        return numpy.array(v)
    elif isinstance(v, tuple):
        return numpy.array(v)
    else:
        raise ValueError(f"Cannot convert {v} to numpy array")


def as_tuple_vec(v: VectorLike) -> Tuple[float, float]:
    if isinstance(v, numpy.ndarray):
        return v[0], v[1]
    elif isinstance(v, list):
        return v[0], v[1]
    elif isinstance(v, tuple):
        return v[0], v[1]
    else:
        raise ValueError(f"Cannot convert {v} to tuple")


def rotate(p: VectorLike, radians: float, center: VectorLike = (0, 0)) -> numpy.ndarray:
    p = as_np_vec(p)
    c = as_np_vec(center)
    v = p - c
    m = numpy.array([[numpy.cos(radians), -numpy.sin(radians)], [numpy.sin(radians), numpy.cos(radians)]])
    return numpy.matmul(m, v) + c


def normalized(v: VectorLike) -> numpy.ndarray:
    v = as_np_vec(v)
    return v / numpy.linalg.norm(v)


def distance(a: VectorLike, b: VectorLike) -> float:
    a = as_np_vec(a)
    b = as_np_vec(b)
    return numpy.linalg.norm(a - b)


def signed_angle_to(a: VectorLike, b: VectorLike) -> float:
    """ Returns the smallest magnitude signed angle which will rotate vector a to the direction of vector b.
    The result will be a value in the range [-pi, pi].  It will be positive if the rotation is in the
    counter-clockwise direction, and negative if the rotation is in the clockwise direction. """
    a = as_np_vec(a)
    b = as_np_vec(b)
    cross = a[0] * b[1] - a[1] * b[0]
    dot = a[0] * b[0] + a[1] * b[1]
    return numpy.arctan2(cross, dot)
