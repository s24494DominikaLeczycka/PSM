# Title: Projectile Motion Simulation with the medium Resistance using Euler and Improved Euler Methods
#
# Description:
# This Python code simulates the motion of a projectile under the influence of gravity and air resistance. The simulation is performed using two numerical methods: Euler's method and Improved Euler's method. The air resistance is assumed to have a linear dependence (Fo = -qV, where q is the drag coefficient in the range of 0 to 1).
#
# The motion takes place along the OX and OY axes; thus, separate equations are calculated for motion in the X and Y directions. The resulting trajectories are displayed as plots, and the total flight time is calculated and displayed in seconds.
#
# The program includes two functions, simulate and simulate1, which correspond to the Euler's method and Improved Euler's method respectively. Each function takes the following parameters:
#
#     initial velocity of the projectile
#     launch angle (in radians)
#     gravitational acceleration (default value: 10 m/s^2)
#     drag coefficient (default value: 0.04)
#     time step for the numerical method (default value: 0.1 s)
#     maximum number of iterations (default value: 10,000)
#
# The main function calls both simulate and simulate1 functions with the same initial velocity and launch angle to compare the results of the two numerical methods. The simulation results are displayed as plots, and the total flight time is printed for each method.

import math

import matplotlib.pyplot as plt


# part 1 - Euler's method
def simulate(velocity, angle, g=10, drag_coefficient=0.04, h=0.1, max_iters=10_000):
    x = [0, ]
    y = [0, ]
    d = drag_coefficient
    v0 = velocity
    vy = [v0 * math.sin(angle), ]
    vx = [v0 * math.sin(angle), ]
    num_iters = 1
    for n in range(1, max_iters):
        if y[n - 1] < 0:
            num_iters = n
            x.pop(-1)
            y.pop(-1)
            vx.pop(-1)
            vy.pop(-1)
            break
        vx.append(vx[n - 1] - h * vx[n - 1] * d)
        x.append(x[n - 1] + h * vx[n - 1])
        vy.append(vy[n - 1] - h * (g + vy[n - 1] * d))
        y.append(y[n - 1] + h * vy[n - 1])
    # draw a plot
    plt.figure(figsize=(20, 10))
    plt.title('Flight trajectory')
    plt.plot(x, y)
    plt.xlabel('distance')
    plt.ylabel('height')
    plt.grid()
    plt.show()

    print('Time of flight = ', h * num_iters, ' seconds')


# part 2 - improved Euler's method
def simulate1(velocity, angle, g=10, drag_coefficient=0.04, h=0.1, max_iters=10_000):
    x = [0, ]
    y = [0, ]
    d = drag_coefficient
    v0 = velocity
    vy = [v0 * math.sin(angle), ]
    vx = [v0 * math.sin(angle), ]
    num_iters = 1
    for n in range(1, max_iters):
        if y[n - 1] < 0:
            num_iters = n
            x.pop(-1)
            y.pop(-1)
            vx.pop(-1)
            vy.pop(-1)
            break
        # Calculate next velocity
        vxn = vx[n - 1] - h * vx[n - 1] * d
        vyn = vy[n - 1] - h * (g + vy[n - 1] * d)

        # Calculate next position
        xn = x[n - 1] + h * (vx[n - 1] + vxn) / 2
        yn = y[n - 1] + h * (vy[n - 1] + vyn) / 2

        # Add new position and velocity to lists
        x.append(xn)
        y.append(yn)
        vx.append(vxn)
        vy.append(vyn)
    # draw a plot
    plt.figure(figsize=(20, 10))
    plt.title('Flight trajectory')
    plt.plot(x, y)
    plt.xlabel('distance')
    plt.ylabel('height')
    plt.grid()
    plt.show()

    print('Time of flight = ', h * num_iters, ' seconds')


def main():
    simulate(40, math.pi / 4)
    simulate1(40, math.pi / 4)


if __name__ == '__main__':
    main()
