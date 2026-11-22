import heapq
from itertools import count

def astar(start, goal_test, neighbors, heuristic):
    """neighbors(state) yields (next_state, step_cost)."""
    tie = count()
    heap = [(heuristic(start), 0, next(tie), start, [start])]
    best = {start: 0}
    while heap:
        _, cost, _, state, path = heapq.heappop(heap)
        if cost != best.get(state):
            continue
        if goal_test(state):
            return path, cost
        for nxt, step in neighbors(state):
            new_cost = cost + step
            if new_cost < best.get(nxt, float("inf")):
                best[nxt] = new_cost
                heapq.heappush(heap, (new_cost + heuristic(nxt), new_cost,
                                      next(tie), nxt, path + [nxt]))
    return None
