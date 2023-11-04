import copy
import sys
import heapq

goal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
p = []
for i in range(3):
    x = list(map(int, input().split()))
    p.append(x)

adj = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def heuristic(p):
    mht = 0
    for i in range(3):
        for j in range(3):
            if p[i][j] != 0:
                r = p[i][j] // 3
                c = p[i][j] % 3
                mht += abs(i - r) + abs(j - c)
    return mht


def valid(r, c):
    if r >= 0 and r < 3 and c >= 0 and c < 3:
        return True
    else:
        return False


class State:
    def __init__(self, p, g, h, parent):
        self.p = copy.deepcopy(p)
        self.g = g
        self.h = h
        self.parent = parent

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)


def is_goal(s):
    return s.p == goal


def hole_index(s):
    for i in range(3):
        for j in range(3):
            if s.p[i][j] == 0:
                return i, j


def successor(s):
    succ = []
    hr, hc = hole_index(s)
    for d in adj:
        i = hr + d[0]
        j = hc + d[1]
        if valid(i, j):
            x = copy.deepcopy(s)
            x.p[hr][hc], x.p[i][j] = x.p[i][j], x.p[hr][hc]
            x.g += 1
            x.h = heuristic(x.p)
            x.parent = s
            succ.append(x)
    return succ


def Astar(s):
    count = 0
    pq = []
    heapq.heappush(pq, s)

    while pq:
        current = heapq.heappop(pq)
        count += 1
        if is_goal(current):
            return current, count

        successors = successor(current)
        for succ in successors:
            heapq.heappush(pq, succ)

    return None, count


def print_path(s, v):
    path = []
    current = v
    while current is not None:
        path.append(current.p)
        current = current.parent
    path.reverse()
    for state in path:
        print_state(state)


def print_state(state):
    for row in state:
        print(*row)
    print()


initial = State(p, 0, heuristic(p), None)
v, count = Astar(initial)
print(v.g, count)
print_path(initial, v)
