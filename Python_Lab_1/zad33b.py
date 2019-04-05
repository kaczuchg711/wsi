from numpy import sqrt
import os

def count_zero_of_a_function(a, b, c):
    delta = b ** 2 - 4 * a * c
    if delta < 0:
        x1 = (-b - sqrt(delta + 0j)) / (2 * a)
        x2 = (-b + sqrt(delta + 0j)) / (2 * a)
        return x1, x2
    elif delta == 0:
        x0 = -b / (2 * a)
        return x0
    else:
        x1 = (-b - sqrt(delta)) / (2 * a)
        x2 = (-b + sqrt(delta)) / (2 * a)
        return x1, x2

a = 1
b = -2
c = 2