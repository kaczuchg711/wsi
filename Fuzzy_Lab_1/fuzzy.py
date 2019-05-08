import numpy as np
import matplotlib.pyplot as plt


#1///////////////////////////////////////////////////////
# pomocnicza funkcja do rysowania zbiorów rozmytych
def plot_fuzzyset(ax, fuzzy_set, x, *args, **kwargs):
    y = np.array([fuzzy_set(e) for e in x])
    ax.plot(x, y,  *args, **kwargs)
    ax.set_ylim(-0.1, 1.1)
    ax.legend()

from fuzzython.fsets.singleton import Singleton
from fuzzython.fsets.triangular import Triangular
from fuzzython.fsets.trapezoid import Trapezoid
from fuzzython.fsets.gaussian import Gaussian
from fuzzython.fsets.pifunction import PiFunction
from fuzzython.fsets.zfunction import ZFunction
from fuzzython.fsets.sfunction import SFunction

A = Singleton(5.0)
# zbiór rozmyty o trójkątnej funkcji przynależności (podajemy współrzędne wierzchołków)
B = Triangular((0,0), (5,1), (10,0))
# zbiór rozmyty o trapezoidalnej funkcji przynależności (podajemy współrzędne wierzchołków)
C = Trapezoid((0,0), (3,1), (7,1), (10,0))
# zbiór rozmyty o gaussowskiej funkcji przynależności (podajemy mean i std)
D = Gaussian(5, 1.5)
# zbiór rozmyty o funkcji przynależności typu S (podajemy punkt dla 0, punkt przegięcia i punkt dla 1)
E = SFunction((5,0), 7.5, (10,1))
# zbiór rozmyty o funkcji przynależności typu Z (podajemy punkt dla 1, punkt przegięcia i punkt dla 0)
# w module jest błąd i trzeba podać odwrotnie drugie współrzędne
F = ZFunction((0,0), 2.5, (5,1))

# wykresy poglądowe
x = np.round(np.linspace(-1,11,2000),2)
fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(12,8))
((ax1, ax2), (ax3, ax4), (ax5, ax6)) = axs
plot_fuzzyset(ax1, A, x, 'k', label='Singleton')
plot_fuzzyset(ax2, B, x, 'k', label='Triangular')
plot_fuzzyset(ax3, C, x, 'k', label='Trapezoid')
plot_fuzzyset(ax4, D, x, 'k', label='Gaussian')
plot_fuzzyset(ax5, E, x, 'k', label='SFunction')
plot_fuzzyset(ax6, F, x, 'k', label='ZFunction')
plt.show()






#2///////////////////////////////////////////////////////

from fuzzython.norms import norms

A = Triangular((0,0), (3,1), (6,0))
B = Triangular((4,0), (7,1), (10,0))
C = A.union(B, snorm=norms.maximum)
D = A.union(B, snorm=norms.algebraic_sum)
E = A.intersect(B, tnorm=norms.minimum)
F = A.intersect(B, tnorm=norms.algebraic_product)
G = A.complement(cnorm=norms.zadeh_complement)
H = B.complement(cnorm=norms.zadeh_complement)

# wykresy poglądowe
x = np.linspace(-1,11,1000)
fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(12,8))
((ax1, ax2, ax3), (ax4, ax5, ax6), (ax7, ax8, ax9)) = axs
plot_fuzzyset(ax1, A, x, 'r', label='A')
plot_fuzzyset(ax1, B, x, 'b', label='B')
plot_fuzzyset(ax2, C, x, 'k', label='max')
plot_fuzzyset(ax3, D, x, 'k', label='asum')
plot_fuzzyset(ax4, A, x, 'r', label='A')
plot_fuzzyset(ax4, B, x, 'b', label='B')
plot_fuzzyset(ax5, E, x, 'k', label='min')
plot_fuzzyset(ax6, F, x, 'k', label='aprod')
plot_fuzzyset(ax7, A, x, 'r', label='A')
plot_fuzzyset(ax7, B, x, 'b', label='B')
plot_fuzzyset(ax8, G, x, 'k', label='Zadeh A')
plot_fuzzyset(ax9, H, x, 'k', label='Zadeh B')
plt.show()






#3///////////////////////////////////////////////////////
from fuzzython.fsets.fuzzy_set import FuzzySet

A = Trapezoid((0,0), (1,1), (3,1), (8,0))
B = Trapezoid((5,0), (6,1), (7,1), (10,0))
C = A.union(B, snorm=norms.algebraic_sum)

cog = FuzzySet.COG(C)
coa = FuzzySet.COA(C)
cm = FuzzySet.CM(C)
mm = FuzzySet.MM(C)
lm = FuzzySet.LM(C)
rm = FuzzySet.RM(C)

# wykresy poglądowe
x = np.linspace(-1,11,1000)
fig, ax = plt.subplots(figsize=(10,6))
plot_fuzzyset(ax, C, x, 'k', label='C')
ax.axvline(x=cog, c='b', label='COG')
ax.axvline(x=coa, c='r', label='COA')
ax.axvline(x=cm, c='g', label='CM')
ax.axvline(x=mm, c='m', label='MM')
ax.axvline(x=lm, c='y', label='LM')
ax.axvline(x=rm, c='c', label='RM')
plt.legend()
plt.show()





#4///////////////////////////////////////////////////////
## Przykład: Model Mamdaniego: Decydujemy o wysokości napiwku
### Definiowanie zmiennych lingwistycznych



# prosty przykład z użyciem trójkątnych zbiorów rozmytych
from fuzzython.fsets.triangular import Triangular
# klasa Variable - zmienna lingwistyczna
from fuzzython.variable import Variable
# klasa Adjective - wartość zmiennej lingwistycznej
from fuzzython.adjective import Adjective

# zmienna lingwistyczna `quality` opisująca jakość jedenia w skali od 0 do 10 gwiazdek (star)
# trzy wartości lingwistyczne, trójkątne zbiory rozmyte: `q_poor`, `q_average`, `q_good`

q_poor = Triangular((-0.1,0), (0,1), (5,0))
q_average = Triangular((0,0), (5,1), (10,0))
q_good = Triangular((5,0), (10,1), (10.1,0))
a_q_poor = Adjective('q_poor', q_poor)
a_q_average = Adjective('q_average', q_average)
a_q_good = Adjective('q_good', q_good)
quality = Variable('quality', 'star', a_q_poor, a_q_average, a_q_good)

# zmienna lingwistyczna `service` opisująca jakość obsługi w skali od 0 do 10 gwiazdek (star)
# trzy wartości lingwistyczne, trójkątne zbiory rozmyte: `s_poor`, `s_average`, `s_good`

s_poor = Triangular((-0.1,0), (0,1), (5,0))
s_average = Triangular((0,0), (5,1), (10,0))
s_good = Triangular((5,0), (10,1), (10.1,0))
a_s_poor = Adjective('s_poor', s_poor)
a_s_average = Adjective('s_average', s_average)
a_s_good = Adjective('s_good', s_good)
service = Variable('service', 'star', a_s_poor, a_s_average, a_s_good)

# zmienna lingwistyczna `tip` opisująca jwysokość napiwku w skali od 0 do 25 procent (%)
# trzy wartości lingwistyczne, trójkątne zbiory rozmyte: `t_low`, `t_medium`, `t_high`

t_low = Triangular((-0.1,0), (0,1), (13,0))
t_medium = Triangular((0,0), (13,1), (25,0))
t_high = Triangular((13,0), (25,1), (25.1,0))
a_t_low = Adjective('t_low', t_low)
a_t_medium = Adjective('t_medium', t_medium)
a_t_high = Adjective('t_high', t_high)
tip = Variable('tip', '%', a_t_low, a_t_medium, a_t_high, defuzzification='COG', default=0)

# wykresy poglądowe
x = np.linspace(0,10,1000)
x2 = np.linspace(0,25,1000)
fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(12,8))
((ax1), (ax2), (ax3)) = axs
plot_fuzzyset(ax1, q_poor, x, 'b', label='q_poor')
plot_fuzzyset(ax1, q_average, x, 'g', label='q_average')
plot_fuzzyset(ax1, q_good, x, 'r', label='q_good')
plot_fuzzyset(ax2, s_poor, x, 'b', label='s_poor')
plot_fuzzyset(ax2, s_average, x, 'g', label='s_average')
plot_fuzzyset(ax2, s_good, x, 'r', label='s_good')
plot_fuzzyset(ax3, t_low, x2, 'b', label='t_low')
plot_fuzzyset(ax3, t_medium, x2, 'g', label='t_medium')
plot_fuzzyset(ax3, t_high, x2, 'r', label='t_high')
plt.show()







#5///////////////////////////////////////////////////////

from fuzzython.ruleblock import RuleBlock

scope = locals()

rule1 = 'if quality is a_q_poor or service is a_s_poor then tip is a_t_low'
rule2 = 'if quality is a_q_average then tip is a_t_medium'
rule3 = 'if quality is a_q_good or service is a_s_good then tip is a_t_high'

# operators - operatory dla przecięcia, sumy i dopełnienia zbiorów rozmytych
# activation - operator dla implikacji
# accumulation - aperator dla agregacji reguł
block = RuleBlock('rb_mamdani', operators=('MIN','MAX','ZADEH'), activation='MIN', accumulation='MAX')
block.add_rules(rule1, rule2, rule3, scope=scope)

from fuzzython.systems.mamdani import MamdaniSystem

mamdani = MamdaniSystem('mamdani_model', block)


# dane wejściowe
inputs = {'quality': 6, 'service': 9} #tak naprawdę to można podać liczby rzeczywiste od 0 do 10
# obliczenie odpowiedzi
res = mamdani.compute(inputs)
#zwraca słownik
res

# %matplotlib notebook
from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting

# przygotowanie siatki
sampled = np.linspace(0, 10, 20)
x, y = np.meshgrid(sampled, sampled)
z = np.zeros((len(sampled), len(sampled)))

for i in range(len(sampled)):
    for j in range(len(sampled)):
        inputs = {'quality': x[i, j], 'service': y[i, j]}
        res = mamdani.compute(inputs)
        z[i, j] = res['rb_mamdani']['tip']

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis', linewidth=0.4, antialiased=True)
cset = ax.contourf(x, y, z, zdir='z', offset=-1, cmap='viridis', alpha=0.5)
cset = ax.contourf(x, y, z, zdir='x', offset=11, cmap='viridis', alpha=0.5)
cset = ax.contourf(x, y, z, zdir='y', offset=11, cmap='viridis', alpha=0.5)
ax.set_xlabel('quality')
ax.set_ylabel('service')
ax.set_zlabel('tip')
ax.view_init(30, 200)
#

rule4 = 'if quality is a_q_poor or service is a_s_poor then z=quality*0.5+service*0.5'
rule5 = 'if quality is a_q_average then z=quality*0.7+5'
rule6 = 'if quality is a_q_good or service is a_s_good then z=quality*0.4+service*0.6+15'

block = RuleBlock('rb_takagi', operators=('MIN', 'MAX', 'ZADEH'), activation='MIN', accumulation='MAX')
block.add_rules(rule4, rule5, rule6, scope=scope)




from fuzzython.systems.sugeno import SugenoSystem

sugeno = SugenoSystem('model_takagi', block)




# dane wejściowe
inputs = {'quality': 6, 'service': 9}
# obliczenie odpowiedzi
res = sugeno.compute(inputs)
# zwraca słownik, trochę inaczej niż w mamdani
res

# %matplotlib notebook
from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting

# przygotowanie siatki
sampled = np.linspace(0, 10, 20)
x, y = np.meshgrid(sampled, sampled)
z = np.zeros((len(sampled), len(sampled)))

for i in range(len(sampled)):
    for j in range(len(sampled)):
        inputs = {'quality': x[i, j], 'service': y[i, j]}
        res = sugeno.compute(inputs)
        z[i, j] = res['rb_takagi']

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis', linewidth=0.4, antialiased=True)
cset = ax.contourf(x, y, z, zdir='z', offset=-1, cmap='viridis', alpha=0.5)
cset = ax.contourf(x, y, z, zdir='x', offset=11, cmap='viridis', alpha=0.5)
cset = ax.contourf(x, y, z, zdir='y', offset=11, cmap='viridis', alpha=0.5)
ax.set_xlabel('quality')
ax.set_ylabel('service')
ax.set_zlabel('tip')
ax.view_init(30, 200)