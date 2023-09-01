import typing as tp


def normalize_path(path: str) -> str:
    """
    :param path: unix path to normalize
    :return: normalized path
    """
    if not len(path):
        return '.'
    while '//' in path:
        path = path.replace('//', '/')

    items = path.split('/')
    stack: tp.List[str] = []
    for name in items:
        # if name == '':
        #     continue
        if len(stack) >= 2 and stack[len(stack) - 1] == '.':
            stack.pop()
        if name == '..':
            if len(stack):
                last = stack[len(stack) - 1]
            if len(stack) and len(last) and last != '.' and last != '..':
                stack.pop()
                continue
            if len(stack) == 1:
                if stack[0] == '':
                    continue
                elif stack[0] == '.':
                    stack.pop()
        if len(stack) and stack[len(stack) - 1] == '.':
            stack.pop()
        stack.append(name)

    # if not len(stack):
    #     return '/'

    norm_path = ''
    for i, path in enumerate(stack):
        if path == '' and i == len(stack) - 1 and len(stack) > 1:
            continue
        norm_path += (path + '/')
    if not len(norm_path):
        return '.'
    print(norm_path)
    if norm_path == '/':
        return norm_path
    return norm_path[:-1]
