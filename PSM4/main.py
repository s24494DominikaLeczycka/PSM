# Project Name: Rolling Objects on Inclined Plane Simulation

# Description: This Python project simulates the motion of two different rolling objects (a ball and a sphere) on an inclined plane using the Midpoint Method. The simulation calculates the position, rotation angle, and optionally, the potential, kinetic, and total energy of the objects over time. The results of the simulation are visualized in the form of graphs showing the change in position, rotation angle, and energy over time.

import numpy as np
import matplotlib.pyplot as plt

# physical constants
alpha = np.deg2rad(10)  # angle of inclination
g = 10.0
m = 1  # mass of the objects
r = 0.1  # radius of the objects
I_kuli = (2/5)*m*r**2  # moment of inertia of the ball
I_sfera = (2/3)*m*r**2  # moment of inertia of the sphere
mu = 0.01  # rolling friction coefficient
slipping_factor = 0.1  # introduce slipping factor (0 to 1)


# initial conditions
L = 5  # length of the inclined plane in meters
s0 = L  # initial position along the inclined plane
v0 = 0  # initial velocity
beta0 = 0  # initial angle of rotation
omega0 = 0  # initial angular velocity

# simulation parameters
t_max = 10
dt = 0.001
t = np.arange(0, t_max, dt)

# midpoint method
def midpoint_sphere(s, v, beta, omega):
    # calculate linear acceleration of a ball
    a_without_friction = g * np.sin(alpha) / (1 + I_sfera / (m * r ** 2))
    rolling_friction = mu * m * g * np.cos(alpha)
    a = a_without_friction - rolling_friction / m
    return midpoint(s, v, beta, omega, a)

def midpoint_ball(s, v, beta, omega):
    # calculate linear acceleration of a ball
    a_without_friction = g * np.sin(alpha) / (1 + I_kuli / (m * r ** 2))
    rolling_friction = mu * m * g * np.cos(alpha)
    a = a_without_friction - rolling_friction / m
    return midpoint(s, v, beta, omega, a)

def midpoint(s, v, beta, omega, a):
    # calculate angular acceleration given linear acceleration
    eps = a/r
    # calculate new values of position and velocity using midpoint method
    s_half = s + v*dt/2
    v_half = v + a*dt/2
    s_new = s + v_half*dt
    v_new = v + a*dt
    # calculate new values of angle of rotation and angular velocity using midpoint method
    beta_half = beta + omega*dt/2
    omega_half = omega + eps*dt/2
    beta_new = beta + omega_half*dt
    omega_new = omega + eps*dt
    return (s_new+s_half)/2, (v_new+v_half)/2, (beta_new+beta_half)/2, (omega_new + omega_half)/2

# function to calculate total energy
def total_energy_sphere(v, s, omega):
    # calculate kinetic and potential energy for both objects
    E_sfera = 0.5 * m * v ** 2 + 0.5 * I_sfera * omega ** 2
    E_pot = m * g * (L - s) * np.sin(alpha)
    # calculate total energy
    E_total_sfera = E_sfera + E_pot
    return E_total_sfera

def total_energy_ball(v, s, omega):
    # calculate kinetic and potential energy for both objects
    E_kuli = 0.5 * m * v ** 2 + 0.5 * I_kuli * omega ** 2
    E_pot = m * g * (L - s) * np.sin(alpha)
    # calculate total energy
    E_total_kuli = E_kuli + E_pot
    return E_total_kuli
def main():
    # initialize arrays to store the results
    s_kuli = np.zeros_like(t)
    v_kuli = np.zeros_like(t)
    beta_kuli = np.zeros_like(t)
    omega_kuli = np.zeros_like(t)
    s_sfera = np.zeros_like(t)
    v_sfera = np.zeros_like(t)
    beta_sfera = np.zeros_like(t)
    omega_sfera = np.zeros_like(t)
    E_total_kuli = np.zeros_like(t)
    E_total_sfera = np.zeros_like(t)

    # set initial values of arrays
    s_kuli[0] = 0
    v_kuli[0] = v0
    beta_kuli[0] = beta0
    omega_kuli[0] = omega0
    s_sfera[0] = 0
    v_sfera[0] = v0
    beta_sfera[0] = beta0
    omega_sfera[0] = omega0
    E_total_kuli[0] = total_energy_ball(v0, beta0, omega0)
    E_total_sfera[0] = total_energy_sphere(v0, beta0, omega0)

    # calculate values using midpoint method
    for i in range(1, len(t)):
        s_kuli[i], v_kuli[i], beta_kuli[i], omega_kuli[i] = midpoint_ball(s_kuli[i-1], v_kuli[i-1], beta_kuli[i-1], omega_kuli[i-1])
        s_sfera[i], v_sfera[i], beta_sfera[i], omega_sfera[i] = midpoint_sphere(s_sfera[i-1], v_sfera[i-1], beta_sfera[i-1], omega_sfera[i-1])
        E_total_kuli[i], E_total_sfera[i] = total_energy_ball(v_kuli[i], s_kuli[i], omega_kuli[i]), total_energy_sphere(v_sfera[i], s_sfera[i], omega_sfera[i])

    # plot results
    plt.figure(figsize=(10, 8))
    plt.subplot(3, 1, 1)
    plt.plot(t, s_kuli, label='Kula')
    plt.plot(t, s_sfera, label='Sfera')
    plt.xlabel('Czas [s]')
    plt.ylabel('Położenie [m]')
    plt.legend()
    plt.subplot(3, 1, 2)
    plt.plot(t, np.rad2deg(beta_kuli), label='Kula')
    plt.plot(t, np.rad2deg(beta_sfera), label='Sfera')
    plt.xlabel('Czas [s]')
    plt.ylabel('Kąt obrotu [deg]')
    plt.legend()
    plt.subplot(3, 1, 3)
    plt.plot(t, E_total_kuli, label='Kula')
    plt.plot(t, E_total_sfera, label='Sfera')
    plt.xlabel('Czas [s]')
    plt.ylabel('Energia [J]')
    plt.legend()
    # add spacing between the subplots
    plt.subplots_adjust(hspace=0.5)
    plt.show()

if __name__ == '__main__':
    main()