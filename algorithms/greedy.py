import heapq
from itertools import count

def greedy_best_first(start, goal_test, neighbors, heuristic):
    tie = count()
    heap = [(heuristic(start), next(tie), start, [start])]
    seen = set()
    while heap:
        _, _, state, path = heapq.heappop(heap)
        if state in seen:
            continue
        if goal_test(state):
            return path
        seen.add(state)
        for nxt in neighbors(state):
            if nxt not in seen:
                heapq.heappush(heap, (heuristic(nxt), next(tie), nxt, path + [nxt]))
    return None
