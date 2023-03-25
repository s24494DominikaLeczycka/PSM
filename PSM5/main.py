# Title: Moon's trajectory Simulation

# Description: The code plots the trajectory of the Moon with respect to the Sun by solving the equations describing the motion of the Earth around the Sun and the Moon with respect to the Earth. Assume Earth moves in a circular orbit, and the Moon moves in a circular orbit with respect to Earth. The improved Euler method (MidPoint) is used to solve the motion equations. This Python program visualizes the trajectories of the Earth and the Moon around the Sun over a year and the distances between the Sun and the Earth/Moon over a year.

import math
import matplotlib.pyplot as plt

G = 6.6743 * (10 ** (-11))
TIME_STEP = 60 * 60 * 24  # 1 day in seconds


class CelestialBody:
    def __init__(self, mass, x, y, vx, vy):
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def force(self, other):
        dist = self.distance(other)
        magnitude = G * self.mass * other.mass / (dist ** 2)
        dx = (other.x - self.x) / dist
        dy = (other.y - self.y) / dist
        return magnitude * dx, magnitude * dy


def midpoint_update_positions(sun, earth, moon):
    fx_earth_moon, fy_earth_moon = earth.force(moon)
    fx_moon_earth, fy_moon_earth = moon.force(earth)
    fx_earth_sun, fy_earth_sun = earth.force(sun)
    fx_moon_sun, fy_moon_sun = moon.force(sun)

    # Compute k1
    k1_x_earth = earth.vx
    k1_y_earth = earth.vy
    k1_vx_earth = (fx_earth_moon + fx_earth_sun) / earth.mass
    k1_vy_earth = (fy_earth_moon + fy_earth_sun) / earth.mass

    k1_x_moon = moon.vx
    k1_y_moon = moon.vy
    k1_vx_moon = (fx_moon_earth + fx_moon_sun) / moon.mass
    k1_vy_moon = (fy_moon_earth + fy_moon_sun) / moon.mass

    # Compute midpoint values
    earth_mid_x = earth.x + 0.5 * k1_x_earth * TIME_STEP
    earth_mid_y = earth.y + 0.5 * k1_y_earth * TIME_STEP
    earth_mid_vx = earth.vx + 0.5 * k1_vx_earth * TIME_STEP
    earth_mid_vy = earth.vy + 0.5 * k1_vy_earth * TIME_STEP

    moon_mid_x = moon.x + 0.5 * k1_x_moon * TIME_STEP
    moon_mid_y = moon.y + 0.5 * k1_y_moon * TIME_STEP
    moon_mid_vx = moon.vx + 0.5 * k1_vx_moon * TIME_STEP
    moon_mid_vy = moon.vy + 0.5 * k1_vy_moon * TIME_STEP

    # Temporarily update positions for force calculations
    earth.x, earth.y = earth_mid_x, earth_mid_y
    moon.x, moon.y = moon_mid_x, moon_mid_y

    fx_earth_moon, fy_earth_moon = earth.force(moon)
    fx_moon_earth, fy_moon_earth = moon.force(earth)
    fx_earth_sun, fy_earth_sun = earth.force(sun)
    fx_moon_sun, fy_moon_sun = moon.force(sun)

    # Restore original positions
    earth.x, earth.y = earth_mid_x - 0.5 * k1_x_earth * TIME_STEP, earth_mid_y - 0.5 * k1_y_earth * TIME_STEP
    moon.x, moon.y = moon_mid_x - 0.5 * k1_x_moon * TIME_STEP, moon_mid_y - 0.5 * k1_y_moon * TIME_STEP

    # Compute k2
    k2_x_earth = earth_mid_vx
    k2_y_earth = earth_mid_vy
    k2_vx_earth = (fx_earth_moon + fx_earth_sun) / earth.mass
    k2_vy_earth = (fy_earth_moon + fy_earth_sun) / earth.mass

    k2_x_moon = moon_mid_vx
    k2_y_moon = moon_mid_vy
    k2_vx_moon = (fx_moon_earth + fx_moon_sun) / moon.mass
    k2_vy_moon = (fy_moon_earth + fy_moon_sun) / moon.mass

    # Update positions and velocities
    earth.vx += k2_vx_earth * TIME_STEP
    earth.vy += k2_vy_earth * TIME_STEP
    moon.vx += k2_vx_moon * TIME_STEP
    moon.vy += k2_vy_moon * TIME_STEP

    earth.x += k2_x_earth * TIME_STEP
    earth.y += k2_y_earth * TIME_STEP
    moon.x += k2_x_moon * TIME_STEP
    moon.y += k2_y_moon * TIME_STEP


def main():
    earth = CelestialBody(5.972 * (10 ** 24), 147.1 * (10 ** 9), 0, 0, 29.29 * (10 ** 3))
    moon = CelestialBody(7.342 * (10 ** 22), 147.1 * (10 ** 9) + 384.4 * (10 ** 6), 0, 0,
                         29.29 * (10 ** 3) + 1.022 * (10 ** 3))
    sun = CelestialBody(1.989 * (10 ** 30), 0, 0, 0, 0)

    days = 365
    earth_distances = []
    moon_distances = []
    earth_x_positions = []
    earth_y_positions = []
    moon_x_positions = []
    moon_y_positions = []

    for _ in range(days):
        earth_distances.append(earth.distance(sun))
        moon_distances.append(moon.distance(sun))
        earth_x_positions.append(earth.x)
        earth_y_positions.append(earth.y)
        moon_x_positions.append(moon.x)
        moon_y_positions.append(moon.y)
        midpoint_update_positions(sun, earth, moon)

    plt.plot(earth_x_positions, earth_y_positions, label="Earth's Trajectory")
    plt.plot(moon_x_positions, moon_y_positions, label="Moon's Trajectory")
    plt.scatter([0], [0], color="yellow", label="Sun")
    plt.xlabel("X Position (m)")
    plt.ylabel("Y Position (m)")
    plt.legend()
    plt.title("Earth's and moon's Trajectories around the Sun over a Year")
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

    plt.plot(range(days), earth_distances, label="Earth-Sun Distance")
    plt.plot(range(days), moon_distances, label="Moon-Sun Distance")
    plt.xlabel("Days")
    plt.ylabel("Distance (m)")
    plt.legend()
    plt.title("Distance between Sun and Earth/Moon over a Year")
    plt.show()


if __name__ == "__main__":
    main()
