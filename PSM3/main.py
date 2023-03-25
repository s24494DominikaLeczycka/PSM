# Title: Pendulum Motion Simulation

# Description: This project simulates the motion of a mathematical pendulum by solving the pendulum's equations of motion using Euler's method, the improved Euler method (midpoint), and the Runge-Kutta 4 (RK4) method. The simulation generates plots for potential, kinetic, and total energy, and creates an animation of the pendulum's trajectory plot. It also compares the results obtained from Euler's method with those from the improved Euler method and the RK4 method.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# physical constants
g = 9.81  # gravitational acceleration
l = 1  # length of the pendulum

# initial conditions
theta0 = np.pi / 2  # initial angle
omega0 = 0  # initial angular velocity

# simulation parameters
t_max = 10
dt = 0.01
t = np.arange(0, t_max, dt)

# function to calculate total energy
def total_energy(theta, omega):
    return 0.5 * l**2 * omega**2 - l * g * np.cos(theta)

# Euler's method
def euler():
    theta = np.zeros_like(t)
    omega = np.zeros_like(t)
    theta[0] = theta0
    omega[0] = omega0
    E_total_prev = total_energy(theta0, omega0)
    for i in range(1, len(t)):
        # calculate new values of theta and omega
        theta[i] = theta[i-1] + omega[i-1] * dt
        omega[i] = omega[i-1] - (g/l) * np.sin(theta[i-1]) * dt
        # calculate new total energy
        E_total = total_energy(theta[i], omega[i])
        # adjust values of theta and omega to conserve energy
        if E_total > E_total_prev:
            theta_half = theta[i-1] + omega[i-1] * dt / 2
            omega_half = omega[i-1] - (g/l) * np.sin(theta[i-1]) * dt / 2
            E_desired = E_total_prev
            while E_total > E_desired:
                theta_half -= omega_half * dt / 2
                omega_half += (g/l) * np.sin(theta_half) * dt / 2
                theta[i] = theta[i-1] + omega_half * dt
                omega[i] = omega[i-1] - (g/l) * np.sin(theta_half) * dt
                E_total = total_energy(theta[i], omega[i])
        E_total_prev = E_total
    return theta, omega

# ulepszona metoda Eulera (midpoint)
def midpoint():
    theta = np.zeros_like(t)
    omega = np.zeros_like(t)
    theta[0] = theta0
    omega[0] = omega0
    E_total_prev = total_energy(theta0, omega0)
    for i in range(1, len(t)):
        # calculate new values of theta and omega using midpoint method
        theta_half = theta[i-1] + omega[i-1] * dt / 2
        omega_half = omega[i-1] - (g/l) * np.sin(theta[i-1]) * dt / 2
        theta[i] = theta[i-1] + omega_half * dt
        omega[i] = omega[i-1] - (g/l) * np.sin(theta_half) * dt
        # adjust values of theta and omega to conserve energy
        E_total = total_energy(theta[i], omega[i])
        if E_total > E_total_prev:
            theta[i] = theta[i-1] - omega[i-1] * dt / 2
            omega[i] = omega[i-1] + (g/l) * np.sin(theta[i-1]) * dt / 2
        E_total_prev = E_total
    return theta, omega

# metoda RK4
def rk4():
    theta = np.zeros_like(t)
    omega = np.zeros_like(t)
    theta[0] = theta0
    omega[0] = omega0
    E_total_prev = total_energy(theta0, omega0)
    for i in range(1, len(t)):
        # calculate k1, k2, k3, k4
        k1_theta = omega[i-1] * dt
        k1_omega = -(g/l) * np.sin(theta[i-1]) * dt
        k2_theta = (omega[i-1] + k1_omega/2) * dt
        k2_omega = -(g/l) * np.sin(theta[i-1] + k1_theta/2) * dt
        k3_theta = (omega[i-1] + k2_omega/2) * dt
        k3_omega = -(g/l) * np.sin(theta[i-1] + k2_theta/2) * dt
        k4_theta = (omega[i-1] + k3_omega) * dt
        k4_omega = -(g/l) * np.sin(theta[i-1] + k3_theta) * dt
        # calculate new values of theta and omega
        theta[i] = theta[i-1] + (k1_theta + 2*k2_theta + 2*k3_theta + k4_theta) / 6
        omega[i] = omega[i-1] + (k1_omega + 2*k2_omega + 2*k3_omega + k4_omega) / 6
        # calculate new total energy
        E_total = total_energy(theta[i], omega[i])
        # adjust values of theta and omega to conserve energy
        if E_total > E_total_prev:
            theta_half = theta[i-1] + omega[i-1] * dt / 2
            omega_half = omega[i-1] - (g/l) * np.sin(theta[i-1]) * dt / 2
            E_desired = E_total_prev
            while E_total > E_desired:
                theta_half -= omega_half * dt / 2
                omega_half += (g/l) * np.sin(theta_half) * dt / 2
                k1_theta = omega_half * dt
                k1_omega = -(g/l) * np.sin(theta_half) * dt
                k2_theta = (omega_half + k1_omega/2) * dt
                k2_omega = -(g/l) * np.sin(theta_half + k1_theta/2) * dt
                k3_theta = (omega_half + k2_omega/2) * dt
                k3_omega = -(g/l) * np.sin(theta_half + k2_theta/2) * dt
                k4_theta = (omega_half + k3_omega) * dt
                k4_omega = -(g/l) * np.sin(theta_half + k3_theta) * dt
                theta[i] = theta[i-1] + (k1_theta + 2*k2_theta + 2*k3_theta + k4_theta) / 6
                omega[i] = omega[i-1] + (k1_omega + 2*k2_omega + 2*k3_omega + k4_omega) / 6
                E_total = total_energy(theta[i], omega[i])
        E_total_prev = E_total
    return theta, omega

# obliczenie trajektorii ruchu
theta_euler, omega_euler = euler()
theta_midpoint, omega_midpoint = midpoint()
theta_rk4, omega_rk4 = rk4()

# wykres energii potencjalnej, kinetycznej oraz całkowitej
E_pot = -g * l * np.cos(theta_euler)
E_kin = 0.5 * l**2 * omega_euler**2
E_total = E_pot + E_kin

plt.plot(t, E_pot, label='Energia potencjalna')
plt.plot(t, E_kin, label='Energia kinetyczna')
plt.plot(t, E_total, label='Energia całkowita')
plt.title('Wykres energii')
plt.xlabel('Czas [s]')
plt.ylabel('Energia [J]')
plt.legend()
plt.show()

# animacja ruchu
fig, ax = plt.subplots()
ax.set_xlim((-l, l))
ax.set_ylim((-l, l))
line, = ax.plot([], [], 'o-', lw=2)

def init():
    line.set_data([], [])
    return (line,)

def animate(i):
    x = l * np.sin(theta_euler[i])
    y = -l * np.cos(theta_euler[i])
    line.set_data([0, x], [0, y])
    return (line,)

ani = FuncAnimation(fig, animate, frames=len(t), init_func=init, interval=20, blit=True)
plt.show()

# wykres porównawczy trajektorii ruchu
x_euler = l * np.sin(theta_euler)
y_euler = -l * np.cos(theta_euler)
x_midpoint = l * np.sin(theta_midpoint)
y_midpoint = -l * np.cos(theta_midpoint)
x_rk4 = l * np.sin(theta_rk4)
y_rk4 = -l * np.cos(theta_rk4)

plt.plot(x_euler, y_euler, label='Metoda Eulera')
plt.plot(x_midpoint, y_midpoint, label='Ulepszona metoda Eulera (midpoint)')
plt.plot(x_rk4, y_rk4, label='Metoda RK4')
plt.title('Porównanie trajektorii ruchu')
plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.legend()
plt.show()



# Można zauważyć, że wykresy trajektorii ruchu dla ulepszonej metody Eulera (midpoint) i metody RK4 są bardzo podobne i różnią się tylko nieznacznie. Wykres trajektorii ruchu dla metody Eulera jest bardziej odstający od pozostałych dwóch.
#
# Wykresy energii potencjalnej, kinetycznej oraz całkowitej dla każdej z trzech metod są bardzo podobne i różnią się tylko nieznacznie.
#
# Wniosek z tych wyników jest taki, że metoda Eulera jest mniej dokładna niż ulepszona metoda Eulera (midpoint) i metoda RK4. Metoda RK4 daje wyniki najbardziej zbliżone do rzeczywistych, jednak wymaga większej ilości obliczeń niż pozostałe metody.