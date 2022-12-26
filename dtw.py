import numpy as np


def dtw(first: list, second: list, d=lambda x, y: abs(x - y)):
    first = np.array(first)
    second = np.array(second)

    matrx = []
    for i in range(len(first)):
        m = []
        for j in range(len(second)):
            m.append(d(first[i], second[j]))
        matrx.append(m)

    for i in range(len(first)):
        for j in range(len(second)):
            if i == 0:
                matrx[i][j] += matrx[i][j - 1]
            elif j == 0:
                matrx[i][j] += matrx[i - 1][j]
            else:
                matrx[i][j] += min(matrx[i - 1][j], matrx[i][j - 1], matrx[i - 1][j - 1])

    x = len(first) - 1
    y = len(second) - 1

    path = [(x, y)]

    while x > 0 or y > 0:
        if x == 0:
            y -= 1
        elif y == 0:
            x -= 1
        else:
            mn = (matrx[x - 1][y], matrx[x][y - 1], matrx[x - 1][y - 1])
            ind = mn.index(min(mn))
            if ind == 0:
                x -= 1
            elif ind == 1:
                y -= 1
            else:
                x -= 1
                y -= 1
        path.append((x, y))

    return sum([d(first[i[0]], second[i[1]]) for i in path])


# print(dtw([1, 2, 3], [1, 2, 3]))
# print(dtw([1, 2, 3], [3, 2, 1]))
#
# import numpy as np
# np.linalg.norm(10, ord=None, axis=None)
