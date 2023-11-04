from itertools import combinations
import time


def comb(n, k, arr):
    min_diff = sum(arr)
    for mask in combinations(arr, k):
        x = sum(mask)
        min_diff = min(min_diff, abs(sum(arr) - 2 * x))
    return min_diff


st = time.process_time()
if __name__ == "__main__":
    n = int(input())
    arr = list(map(int, input().split()))

    k = n // 2
    min_diff = sum(arr)

    for i in range(1, k + 1):
        temp = comb(n, i, arr)
        min_diff = min(min_diff, temp)

    print(min_diff)
et = time.process_time()
print(et - st)
