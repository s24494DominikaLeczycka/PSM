# Description:
# This Python code implements a sin(x) function using the Taylor Series expansion formula:
#
# sin(x) = x - x^3/3! + x^5/5! - x^7/7! + ...
#
# The function takes an angle x and the number of terms n in the series, and can also accept input in degrees. The function calculates the sin(x) value using the Taylor Series expansion, taking into consideration 1 to n terms in the series. The resulting values are then compared to the sin(x) value obtained using Python's built-in math.sin(x) function, and the absolute difference between these values is displayed.
#
# The code handles cases for input angles in degrees or radians, and it also efficiently calculates sin(x) for angles greater than 2 * pi by reducing the input angle to an equivalent angle within the first quadrant (0 to pi/2) to improve the accuracy of the Taylor Series approximation.

import math


def sin(x, n, degrees=False):
    if degrees:
        x = x * math.pi / 180

    if x >= 2 * math.pi:
        x = x % (2 * math.pi)
    if x > math.pi / 2 and x <= math.pi:
        x = math.pi - x
    elif x > math.pi and x <= 3 / 2 * math.pi:
        x = x - math.pi
    elif x > 3 / 2 * math.pi:
        x = 2 * math.pi - x
    sum = 0
    count = 0
    for exp in range(1, 2 * n, 2):
        sum += (-1) ** count * x ** exp / math.factorial(exp)
        count = count + 1
    return sum


def main():
    x = math.pi / 2
    print('Wynik math.sin(', x, '): ', math.sin(x))
    for n in range(1, 10):
        print('Wynik szeregu Taylora dla ', n, ' pierwszych wyrazów:', sin(x, n))
        print('Wartość bezwzględna różnicy pomiędzy wynikami: ', abs(math.sin(x) - sin(x, n)))


main()
