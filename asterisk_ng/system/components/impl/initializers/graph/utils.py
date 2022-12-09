from collections import defaultdict

from typing import AbstractSet
from typing import MutableSequence
from typing import Sequence
from typing import TypeVar

from .Graph import Graph
from .exceptions import CycleFoundException
from .exceptions import CycleNotFoundException


__all__ = [
    "get_cycle",
    "topological_sort",
]


T = TypeVar('T')


def get_vertexes(graph: Graph[T]) -> AbstractSet[T]:
    vertexes = set(graph.keys())
    vertexes.update(*graph.values())
    return vertexes


def normalize_graph(graph: Graph[T]) -> Graph[T]:
    normalized_graph = defaultdict(set)
    normalized_graph.update(graph)
    return normalized_graph


def reverse_graph(graph: Graph[T]) -> Graph[T]:
    return {vv: {k} for k, v in graph.items() for vv in v}


def get_cycle(graph: Graph[T]) -> Sequence[T]:

    normalized_graph = normalize_graph(graph)
    used_vertexes = set()
    cycle: MutableSequence[T] = []

    def dfs(vertex: T) -> None:
        if vertex in used_vertexes:
            raise CycleFoundException()

        cycle.append(vertex)
        used_vertexes.add(vertex)

        for child_vertex in normalized_graph[vertex]:
            dfs(child_vertex)

        cycle.pop()

    for root in get_vertexes(graph):
        used_vertexes.clear()
        cycle.clear()

        try:
            dfs(root)
        except CycleFoundException:
            return cycle

    raise CycleNotFoundException()


def topological_sort(graph: Graph[T]) -> Sequence[T]:
    normalized_reversed_graph = normalize_graph(reverse_graph(graph))
    used_vertexes = set()
    sequence = []

    def sort(vertex: T) -> None:

        used_vertexes.add(vertex)

        for child_vertex in normalized_reversed_graph[vertex]:
            if child_vertex not in used_vertexes:
                sort(child_vertex)
            elif child_vertex not in sequence:
                raise CycleFoundException()

        sequence.insert(0, vertex)

    for vertex in get_vertexes(graph):
        if vertex not in used_vertexes:
            sort(vertex)

    return sequence
