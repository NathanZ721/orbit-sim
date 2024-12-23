import math
import sys

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

M = [5.683e26, 8.66e25, 1.898e27, 1.988e30, 1.027e26, 1.309e22, 6.39e23, 4.867e24, 3.285e23,
     5.972e24]  # masses of bodies
x = [[1.357e12, 0, -1.303e11], [2.732e12, 0, -3.083e11], [7.41e11, 0, -7.961e10], [0, 0, 0], [4.471e12, 0, -5.007e11],
     [4.434e12, 0, 9.128e11], [2.067e11, 0, -2.035e10], [1.075e11, 0, -7.237e9], [4.6e10, 0, -2.712e9],
     [1.471e11, 0, -1.832e10]]  # initial positions (x, y, z)
v = [[0, 1.014e4, 0], [0, 7.13e3, 0], [0, 1.372e4, 0], [0, -16.79, 0], [0, 5.47e3, 0], [0, 6.1e3, 0], [0, 2.65e4, 0],
     [0, 3.526e4, 0], [0, 5.897e4, 0], [0, 3.029e4, 0]]  # initial velocities (x, y, z)
G, p, t = (6.6743e-11, 0, 0)
h = 3.7e5  # time step in seconds
s = 10  # number of steps per plot point
T = 1e10  # total time to run simulation for (seconds)
p_list = ([[[] for a in range(len(x))] for b in range(3)])

figure = plt.figure(figsize=(12, 7))
ax = figure.add_subplot(projection='3d')
figure.subplots_adjust()


def f(i, pos):
    result = [0, 0, 0]
    for j in range(len(x)):
        if not j == i:
            a = G * M[j] / ((x[j][0] - pos[0]) ** 2 + (x[j][1] - pos[1]) ** 2 + (x[j][2] - pos[2]) ** 2) ** 1.5
            for k in range(3):
                result[k] += (x[j][k] - pos[k]) * a
    return result


mass_slider = Slider(plt.axes([0.05, 0.10, 0.02, 0.80]), 'M', 22, 32, valinit=math.log10(M[p]), orientation='vertical')
vx_slider = Slider(plt.axes([0.10, 0.10, 0.02, 0.80]), 'Vx', -1e5, 1e5, valinit=v[p][0], orientation='vertical')
vy_slider = Slider(plt.axes([0.15, 0.10, 0.02, 0.80]), 'Vy', -1e5, 1e5, valinit=v[p][1], orientation='vertical')
vz_slider = Slider(plt.axes([0.20, 0.10, 0.02, 0.80]), 'Vz', -1e4, 1e4, valinit=v[p][2], orientation='vertical')
planet = Slider(plt.axes([0.88, 0.10, 0.02, 0.80]), 'planet', 0, 9, valinit=p, orientation='vertical', valstep=1)
h_slider = Slider(plt.axes([0.95, 0.10, 0.02, 0.80]), 'time step', 0, 2e6, valinit=h, orientation='vertical')


def update_m(val):
    M[p] = pow(10, mass_slider.val)


def update_x(val):
    v[p][0] = vx_slider.val


def update_y(val):
    v[p][1] = vy_slider.val


def update_z(val):
    v[p][2] = vz_slider.val


def update_h(val):
    global h
    h = h_slider.val


def update_p(val):
    global p
    p = planet.val
    mass_slider.set_val(math.log10(M[p]))


mass_slider.on_changed(update_m)
vx_slider.on_changed(update_x)
vy_slider.on_changed(update_y)
vz_slider.on_changed(update_z)
planet.on_changed(update_p)
h_slider.on_changed(update_h)


def animation_function(a):
    global t
    t += h
    if a % s == 0:
        ax.clear()
        ax.axis('equal')
    for i in range(len(x)):
        f1 = f(i, x[i])
        j1 = [a * h for a in f1]
        k1 = [a * h for a in v[i]]
        f2 = f(i, [x[i][a] + k1[a] / 2 for a in range(3)])
        j2 = [a * h for a in f2]
        k2 = [h * (v[i][a] + j1[a] / 2) for a in range(3)]
        f3 = f(i, [x[i][a] + k2[a] / 2 for a in range(3)])
        j3 = [a * h for a in f3]
        k3 = [h * (v[i][a] + j2[a] / 2) for a in range(3)]
        f4 = f(i, [x[i][a] + k3[a] for a in range(3)])
        j4 = [a * h for a in f4]
        k4 = [h * (v[i][a] + j3[a]) for a in range(3)]
        v[i] = [v[i][a] + 1 / 6 * (j1[a] + 2 * j2[a] + 2 * j3[a] + j4[a]) for a in range(3)]
        x[i] = [x[i][a] + 1 / 6 * (k1[a] + 2 * k2[a] + 2 * k3[a] + k4[a]) for a in range(3)]
        for k in range(3):
            p_list[k][i].append(x[i][k])
        if a % s == 0 and t < T:
            ax.plot(p_list[0][i], p_list[1][i], p_list[2][i], linewidth=1)
            ax.plot(x[i][0], x[i][1], x[i][2], marker='o')
            sys.stdout.write("\r" + str(a * h))
            sys.stdout.flush()
    vx_slider.set_val(v[p][0])
    vy_slider.set_val(v[p][1])
    vz_slider.set_val(v[p][2])


animation = FuncAnimation(figure, animation_function, frames=1000000000, interval=0)
plt.show()
