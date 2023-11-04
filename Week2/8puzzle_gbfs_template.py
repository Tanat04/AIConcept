import copy
from simplePriorityQueue import Simple_Priority_Queue

goal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

p = []
for i in range(3):
    x = list(map(int, input().split()))
    p.append(x)


adj = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def manhattan(p):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = p[i][j]
            if value != 0:
                goal_row, goal_col = divmod(value, 3)
                distance += abs(i - goal_row) + abs(j - goal_col)
    return distance


def heuristic(p):
    return manhattan(p)


def valid(r, c):
    if 0 <= r < 3 and 0 <= c < 3:
        return True
    else:
        return False


class State:
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


def gbfs(s):  # Greedy Best-first Search
    global count
    open_set = Simple_Priority_Queue(cmp=lambda x, y: x.h < y.h)
    open_set.enqueue(s)
    count += 1
    closed_set = set()
    while not open_set.empty():
        current = open_set.dequeue()
        if is_goal(current):
            return current
        closed_set.add(tuple(tuple(row) for row in current.p))
        for neighbor in successor(current):
            if tuple(tuple(row) for row in neighbor.p) not in closed_set:
                open_set.enqueue(neighbor)
                count += 1
    return None


def print_path(s, v):  # s is the initial state, v is the current state
    pass


count = 0
initial = State(p)
v = gbfs(initial)
print(v.g, count)
print_path(initial, v)
