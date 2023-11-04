
'''
Input format:
   line 1: number of time steps
   subsequent lines:
      the room that becomes dirty (0 for A, 1 for B, -1 for nothing happen)

'''

n = int(input())
room = 0   # in room A
dirty = [0,0]
count = 0
for t in range(n):
    r = int(input())
    if r != -1:
        dirty[r] = 1
        if dirty[room] == 0:
            room = (room+1)%2
            count += 1
    if dirty[room] == 1:
        dirty[room] = 0   # sucked
        count += 1
    print(dirty)
print(n, count)
