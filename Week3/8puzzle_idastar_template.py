
import copy
import sys
sys.setrecursionlimit(20000)
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
                r = p[i][j]//3
                c = p[i][j] % 3
                mht += abs(i-r) + abs(j-c)
    return mht


def valid(r, c):
    if r >= 0 and r < 3 and c >= 0 and c < 3:
        return True
    else:
        return False


class state:
    def __init__(self, p):
        self.p = copy.deepcopy(p)
        self.g = 0
        self.h = heuristic(p)
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
            x.h = heuristic(x.p)
            succ.append(x)
    return succ


def DFS(s, atMost):
    global count, found

    if s.g+s.h > atMost:
        return s
    elif is_goal(s):
        found = True
        return s
    else:
        count += 1
        successors = successor(s)
        for succ in successors:
            v = DFS(succ, atMost)
            if found:
                return v
        return None


def IDastar(s):
    global found

    threshold = s.h
    while True:
        result = DFS(s, threshold)
        if found:
            return result
        threshold = sys.maxsize


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


found = False
count = 0
initial = state(p)
v = IDastar(initial)
print(v.g, count)
print_path(initial, v)
