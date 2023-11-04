import sys
import copy
from collections import deque

goal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

p = []   # the input pattern
for i in range(3):
    x = list(map(int, input().split()))
    p.append(x)

print("pattern: ", p)
# relative positions around a position
adj = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def valid(r, c):
    if 0 <= r < 3 and 0 <= c < 3:
        return True
    else:
        return False


class state:
    def __init__(self, p):
        self.p = copy.deepcopy(p)   # the board pattern
        self.g = 0                  # the number of moves so far
        self.parent = None          # the parent state


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


def successor(s):  # generates list of successor states of s
    succ = []
    hr, hc = hole_index(s)
    print("hole location ", hr, hc)
    for d in adj:
        dr, dc = d
        r, c = hr + dr, hc + dc
        # print("where to ", dr, dc)
        print(dr, dc, hr, hc, r, c)
        if valid(r, c):
            x = copy.deepcopy(s)
            # Swap x's tile at position r,c with the hole
            x.p[hr][hc], x.p[r][c] = x.p[r][c], x.p[hr][hc]
            # Record one additional move
            x.g += 1
            # Set the parent state
            x.parent = s
            # Add x to the successor list
            succ.append(x)
    if len(succ):
        for x in succ:
            print("new pattern: ", x.p)
    return succ


def bfs(s):
    count = 0
    queue = deque()
    queue.append(s)
    print()
    # print("Printing out s(First pattern?)")
    # for element in queue:
    #     print(element.p, element.parent, element.g)
    # print()
    visited = set()
    visited.add(tuple(map(tuple, s.p)))
    print("Visited: ", visited)
    print()

    while queue:
        current_state = queue.popleft()
        print("Current state: ", current_state.p,
              current_state.g)

        count += 1

        if is_goal(current_state):
            print("Goal: ", current_state.g, count)
            return current_state, count

        for succ_state in successor(current_state):
            if tuple(map(tuple, succ_state.p)) not in visited:
                queue.append(succ_state)
                visited.add(tuple(map(tuple, succ_state.p)))

    return None, count


def print_path(s, v):  # s is the initial state, v is the current state
    path = []
    while v != s:
        path.append(v)
        v = v.parent

    path.append(s)

    for state in reversed(path):
        for row in state.p:
            print(*row)
        print()


initial = state(p)
v, count = bfs(initial)

# prints the number of moves and total number of states generated
print(v.g, count)
print_path(initial, v)
