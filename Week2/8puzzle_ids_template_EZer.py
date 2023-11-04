import sys
import copy
goal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

p = []
for i in range(3):
    x = list(map(int, input().split()))
    p.append(x)


adj = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def valid(r, c):
    if 0 <= r < 3 and 0 <= c < 3:
        return True
    else:
        return False


class State:
    def __init__(self, p):
        self.p = copy.deepcopy(p)
        self.g = 0
        self.parent = None


def is_goal(s):
    if s.p == goal:
        return True
    else:
        return False


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
            x.parent = s
            x.g += 1
            succ.append(x)
    return succ


def DFS(s, maxDepth):
    global count

    if s.g > maxDepth:
        return None
    elif is_goal(s):
        return s
    else:
        count += 1
        found = False
        minsteps = float('inf')
        for u in successor(s):
            v = DFS(u, maxDepth)
            if v is not None:
                return v
        return None


def IDS(s):
    depth = 0
    while True:
        v = DFS(s, depth)
        if v is not None:
            return v
        depth += 1


def print_path(s, v):
    path = []
    current = v
    while current != s:
        path.append(current)
        current = current.parent
    path.append(s)
    for state in reversed(path):
        for row in state.p:
            print(row)
        print()


count = 0
initial = State(p)
v = IDS(initial)
print(v.g, count)
print_path(initial, v)
