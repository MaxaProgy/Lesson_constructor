"""n, x = map(int, input().split())
list_ac = ["C", "C#", 'D', "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
for i in range(n):
    if i % 2 == 0:
        new_ac = []
        for ac in input().split():
            if list_ac.index(ac) + x < 12:
                new_ac.append(list_ac[list_ac.index(ac) + x])
            else:
                new_ac.append(list_ac[12 - (list_ac.index(ac) + x)])
        print(*new_ac)
    else:
        print(input())"""

"""list_ = []

"""

m, n, q = map(lambda x: int(x), input().split())
tb = [(x, y) for x in range(m + 1) for y in range(n + 1)]
for i in range(q):
    x, y, k = map(lambda x: int(x), input().split())
    house = (x, y)
    print(sum(map(lambda el: 1 if abs(el[0] - house[0]) + abs(el[1] - house[1]) <= k else 0, tb)))