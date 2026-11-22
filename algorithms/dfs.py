def dfs(start, goal_test, neighbors, max_depth=1000):
    """Generic depth-first search. Returns a path or None."""
    stack = [(start, [start])]
    seen = set()
    while stack:
        state, path = stack.pop()
        if goal_test(state):
            return path
        if state in seen or len(path) > max_depth:
            continue
        seen.add(state)
        for nxt in neighbors(state):
            if nxt not in seen:
                stack.append((nxt, path + [nxt]))
    return None
