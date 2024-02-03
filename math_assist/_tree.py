"""
    This module contains tools for better working with the sympy expression tree
"""
from __future__ import annotations

from typing import Optional, List, Union

import sympy
from dataclasses import dataclass


@dataclass
class Node:
    item: sympy.Basic
    children: List[Node]
    parent: Optional[Node] = None

    @property
    def func_type(self) -> type:
        return self.item.func

    def children_except(self, index: int) -> List[Node]:
        return [c for i, c in enumerate(self.children) if i != index]

    def index_of_child(self, child: Node) -> int:
        for i, c in enumerate(self.children):
            if c is child:
                return i
        raise ValueError("Child not found in parent's children")

    def route_from_root(self) -> List[RouteNode]:
        route = []
        child = self
        parent = self.parent
        while parent is not None:
            route.append(RouteNode(parent, parent.index_of_child(child)))
            child = parent
            parent = parent.parent
        route.reverse()
        return route


@dataclass
class RouteNode:
    node: Node
    arg_index: int

    @property
    def next_child(self) -> Node:
        return self.node.children[self.arg_index]

    def other_children(self) -> List[Node]:
        return self.node.children_except(self.arg_index)


class ExpressionTree:
    def __init__(self, root_node: Union[sympy.Basic, Node]):
        if isinstance(root_node, sympy.Basic):
            self._root = _parse_tree(root_node)
        elif isinstance(root_node, Node):
            self._root = root_node
        else:
            raise ValueError("root_node must be a sympy.Basic or a Node")

    @property
    def root(self) -> Node:
        return self._root

    def find_type(self, item_type: type) -> List[Node]:
        results = []

        def _find_type(node: Node):
            if isinstance(node.item, item_type):
                results.append(node)
            for child in node.children:
                _find_type(child)

        _find_type(self.root)

        return results


def _parse_tree(root_node: sympy.Basic, parent: Optional[Node] = None) -> Node:
    node = Node(root_node, [], parent)
    for arg in root_node.args:
        node.children.append(_parse_tree(arg, node))

    return node
