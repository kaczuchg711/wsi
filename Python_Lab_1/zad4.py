import numpy as np


class Figura():

    def licz_pole(self):
        pass

    def licz_obwod(self):
        pass

    def pokaz_pole(self):
        pass

    def pokaz_obwod(self):
        pass


class Trojkat(Figura):
    def __init__(self, a, b, c):
        if a < 0 or b < 0 or c < 0 or a + b < c or a + c < b or b + c < a: raise NotImplementedError()
        self.a = a
        self.b = b
        self.c = c
        self.obwod = self.licz_obwod()
        self.pole = self.licz_pole

    def licz_pole(self):
        p = self.obwod / 2
        pole = np.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))
        return pole

    def licz_obwod(self):
        obwod = self.a + self.b + self.c
        return obwod

    def pokaz_pole(self):
        print(self.pole)

    def pokaz_obwod(self):
        print(self.obwod)


class Prostokat(Figura):
    def __init__(self, a, b):
        if a <= 0 or b <= 0: raise NotImplementedError()
        self.a = a
        self.b = b
        self.obwod = self.licz_obwod()
        self.pole = self.licz_pole()

    def licz_pole(self):
        pole = self.a * self.b
        return pole

    def licz_obwod(self):
        obwod = 2 * self.a + 2 * self.b
        return obwod

    def pokaz_pole(self):
        print(self.pole)

    def pokaz_obwod(self):
        print(self.obwod)


class Kwadrat(Figura):
    def __init__(self, a):
        if a < 0: raise NotImplementedError()
        self.a = a
        self.pole = self.licz_pole()
        self.obwod = self.licz_obwod()

    def licz_pole(self):
        pole = self.a ** 2
        return pole

    def licz_obwod(self):
        obwod = self.a * 4
        return obwod

    def pokaz_pole(self):
        print(self.pole)

    def pokaz_obwod(self):
        print(self.obwod)

