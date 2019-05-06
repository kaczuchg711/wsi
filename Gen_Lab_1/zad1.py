import math

def nbits(a, b, dx):
    # YOUR CODE HERE
    liczba_przedzialow = math.ceil((b - a) / dx)
    dx_new = (b - a) / liczba_przedzialow
    B = (liczba_przedzialow + 1).bit_length()
    return B, dx_new

nbits(1, 2, 0.3)

def gen_population(P, N, B):
