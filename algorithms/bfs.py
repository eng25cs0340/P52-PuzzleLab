from collections import deque

def bfs(start, goal_test, neighbors):
    """Generic breadth-first search. Returns a path or None."""
    queue = deque([(start, [start])])
    seen = {start}
    while queue:
        state, path = queue.popleft()
        if goal_test(state):
            return path
        for nxt in neighbors(state):
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, path + [nxt]))
    return None
