# simulation of a string behaviour using string equation and the midpoint method

from math import pi, sin
import matplotlib.pyplot as plt

import numpy as np

L = pi
n = 10
dt = 0.3
dx = L / n
m = dx
iters = 10
k = 1 # naprężenie / gęstość

def euler():
    print(np.convolve([1, 2, 3, 4, 5], [100, 10, 1][::-1], 'same'))

    xs = np.linspace(0, L, n + 1)
    ys = np.sin(xs)
    vs = np.zeros(n + 1)
    accs = np.zeros(n + 1)
    accs[1:n] = (np.convolve(ys, [1, -2, 1], 'same') / dx ** 2)[1:n]

    Eks = [m / 2 * np.sum(vs ** 2)]
    Eps = [k / (2 * dx) * np.sum(ys ** 2)]
    Ecs = [Eks[-1] + Eps[-1]]

    yy = [ys, ]
    vv = [vs, ]
    aa = [accs, ]

    for iter in range(iters):
        ys = yy[iter] + vv[iter] * dt
        vs = vv[iter] + aa[iter] * dt
        accs = np.zeros(n + 1)
        accs[1:n] = (np.convolve(ys, [1, -2, 1], 'same') / dx ** 2)[1:n]

        yy.append(ys)
        vv.append(vs)
        aa.append(accs)

    for ys in yy:
        plt.plot(np.arange(len(ys)), ys, label="Positions of the string's points in each iteration")
        plt.title("Positions of the string's points in each iteration")
    plt.show()

    for i in range(len()):
        print(f't{i}: {[i]}')
euler()