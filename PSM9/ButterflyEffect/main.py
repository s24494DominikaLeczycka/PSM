# Simulation of a butterfly effect using euler's, midpoint (aka improved euler's) and rk4 (Runge-Kutta) methods

import numpy as np
import matplotlib.pyplot as plt

# Constants
A = 10
B = 25
C = 8/3
dt = 0.003
t_end = 30  # Define an end time

# Initial conditions
x_0 = 1
y_0 = 1
z_0 = 1

# System of equations
def f(t, x, y, z):
    dxdt = A*y - A*x
    dydt = -x*z + B*x - y
    dzdt = x*y - C*z
    return dxdt, dydt, dzdt

# Euler's method
def euler(t, dt, x, y, z):
    dxdt, dydt, dzdt = f(t, x, y, z)
    x += dxdt * dt
    y += dydt * dt
    z += dzdt * dt
    return x, y, z

# Midpoint method
def midpoint(t, dt, x, y, z):
    dxdt, dydt, dzdt = f(t, x, y, z)
    x_mid = x + dxdt * dt / 2
    y_mid = y + dydt * dt / 2
    z_mid = z + dzdt * dt / 2
    dxdt_mid, dydt_mid, dzdt_mid = f(t + dt / 2, x_mid, y_mid, z_mid)
    x += dxdt_mid * dt
    y += dydt_mid * dt
    z += dzdt_mid * dt
    return x, y, z

# Runge-Kutta method (RK4)
def rk4(t, dt, x, y, z):
    dxdt1, dydt1, dzdt1 = f(t, x, y, z)
    dxdt2, dydt2, dzdt2 = f(t + dt / 2, x + dxdt1 * dt / 2, y + dydt1 * dt / 2, z + dzdt1 * dt / 2)
    dxdt3, dydt3, dzdt3 = f(t + dt / 2, x + dxdt2 * dt / 2, y + dydt2 * dt / 2, z + dzdt2 * dt / 2)
    dxdt4, dydt4, dzdt4 = f(t + dt, x + dxdt3 * dt, y + dydt3 * dt, z + dzdt3 * dt)
    x += (dxdt1 + 2 * dxdt2 + 2 * dxdt3 + dxdt4) * dt / 6
    y += (dydt1 + 2 * dydt2 + 2 * dydt3 + dydt4) * dt / 6
    z += (dzdt1 + 2 * dzdt2 + 2 * dzdt3 + dzdt4) * dt / 6
    return x, y, z

def main():
    # Constants
    A = 10
    B = 25
    C = 8 / 3
    dt = 0.003
    t_end = 30  # Define an end time

    # Initial conditions
    x_0 = 1
    y_0 = 1
    z_0 = 1

    # Time array
    t = np.arange(0, t_end, dt)

    # Results storage
    x_euler, y_euler, z_euler = np.zeros_like(t), np.zeros_like(t), np.zeros_like(t)
    x_midpoint, y_midpoint, z_midpoint = np.zeros_like(t), np.zeros_like(t), np.zeros_like(t)
    x_rk4, y_rk4, z_rk4 = np.zeros_like(t), np.zeros_like(t), np.zeros_like(t)

    # Set initial conditions
    x_euler[0], y_euler[0], z_euler[0] = x_0, y_0, z_0
    x_midpoint[0], y_midpoint[0], z_midpoint[0] = x_0, y_0, z_0
    x_rk4[0], y_rk4[0], z_rk4[0] = x_0, y_0, z_0

    # Time-stepping loop
    for i in range(1, t.shape[0]):
        x_euler[i], y_euler[i], z_euler[i] = euler(t[i - 1], dt, x_euler[i - 1], y_euler[i - 1], z_euler[i - 1])
        x_midpoint[i], y_midpoint[i], z_midpoint[i] = midpoint(t[i - 1], dt, x_midpoint[i - 1], y_midpoint[i - 1],
                                                               z_midpoint[i - 1])
        x_rk4[i], y_rk4[i], z_rk4[i] = rk4(t[i - 1], dt, x_rk4[i - 1], y_rk4[i - 1], z_rk4[i - 1])

    # Plotting
    plt.figure(figsize=(15, 10))

    plt.subplot(1, 3, 1)
    plt.plot(x_euler, z_euler)
    plt.title("Euler's method")

    plt.subplot(1, 3, 2)
    plt.plot(x_midpoint, z_midpoint)
    plt.title("Midpoint method")

    plt.subplot(1, 3, 3)
    plt.plot(x_rk4, z_rk4)
    plt.title("Runge-Kutta method (RK4)")

    plt.show()

if __name__ == '__main__':
    main()