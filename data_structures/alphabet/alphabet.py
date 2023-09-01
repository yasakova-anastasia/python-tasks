import enum
import typing as tp


class Status(enum.Enum):
    NEW = 0
    EXTRACTED = 1
    FINISHED = 2


def extract_alphabet(
        graph: dict[str, set[str]]
        ) -> list[str]:
    """
    Extract alphabet from graph
    :param graph: graph with partial order
    :return: alphabet
    """
    used = {v: 0 for v in graph}

    result = []

    def dfs(edge: str) -> None:
        used[edge] = 1
        for new_edge in graph[edge]:
            if not used[new_edge]:
                dfs(new_edge)
        used[edge] = 2
        result.append(edge)

    for k in graph:
        if not used[k]:
            dfs(k)

    result.reverse()

    return result


def build_graph(
        words: list[str]
        ) -> dict[str, set[str]]:
    """
    Build graph from ordered words. Graph should contain all letters from words
    :param words: ordered words
    :return: graph
    """
    result: dict[str, set[str]] = {}
    for i in range(len(words) - 1):
        s1: list[tp.Any] = []
        s2: list[tp.Any] = []
        for j in words[i]:
            s1.append(j)

        for j in words[i + 1]:
            if len(s2) >= len(s1):
                break

            s2.append(j)

        for j1, j2 in zip(s1, s2):
            if j1 != j2:
                if result.get(j1) is not None:
                    result[j1].add(j2)
                else:
                    result[j1] = set()
                    result[j1].add(j2)
                break

    for i, val in enumerate(words):
        for j in val:
            if result.get(j) is None:
                result[j] = set()

    return result


#########################
# Don't change this code
#########################

def get_alphabet(
        words: list[str]
        ) -> list[str]:
    """
    Extract alphabet from sorted words
    :param words: sorted words
    :return: alphabet
    """
    graph = build_graph(words)
    return extract_alphabet(graph)

#########################
