import dis
import types


def count_operations(source_code: types.CodeType) -> dict[str, int]:
    """Count byte code operations in given source code.

    :param source_code: the bytecode operation names to be extracted from
    :return: operation counts
    """
    res = {}
    instructions = dis.get_instructions(source_code)
    stack = []
    for i in instructions:
        stack.append(i)
    while len(stack) != 0:
        i = stack[-1]
        stack.pop()
        if isinstance(i.argval, types.CodeType):
            inst = dis.get_instructions(i.argval)
            for j in inst:
                stack.append(j)
        name = i.opname
        if name not in res:
            res[name] = 1
        else:
            res[name] += 1
    return res
