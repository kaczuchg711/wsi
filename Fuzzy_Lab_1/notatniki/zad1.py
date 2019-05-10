# zad1
import numpy as np
import matplotlib.pyplot as plt


from fuzzython.variable import Variable
from fuzzython.adjective import Adjective
from fuzzython.fsets.triangular import Triangular
from fuzzython.fsets.trapezoid import Trapezoid
from fuzzython.fsets.gaussian import Gaussian
from fuzzython.fsets.zfunction import ZFunction

def plot_fuzzyset(ax, fuzzy_set, x, *args, **kwargs):
    y = np.array([fuzzy_set(e) for e in x])
    ax.plot(x, y, *args, **kwargs)
    ax.set_ylim(-0.1, 1.1)
    ax.legend()


# zmienna lingwistyczna `speed` opisująca prędkośc jazdy od 10 do 200 kmph
# cztery wartości lingwistyczne, zbiory rozmyte: `s_low`, `s_medium`, `s_hight` ,`s_very_hight`

#                                           prędkość

s_low = ZFunction((10, 0), 34, (60, 1))
s_medium = Gaussian(75, 20, 1)
s_high = Gaussian(100, 20, 1)
s_very_high = Trapezoid((120,0),(130,1),(199,1),(200,1))

a_s_low = Adjective('s_low', s_low)
a_s_medium = Adjective('s_medium', s_medium)
a_s_high = Adjective('s_high', s_high)
a_s_very_high = Adjective('s_very_high', s_very_high)
speed = Variable('speed', 'kmph', a_s_low, a_s_medium,a_s_high, a_s_very_high)

# zmienna lingwistyczna `visibility` opisująca widoczność w km  (0.05 − 4km
# trzy wartości lingwistyczne,  zbiory rozmyte: `v_low`, `v_medium`, `v_high`

#                                           widoczność

v_low = Gaussian(0, 1, 1)
v_medium = Gaussian(2, 1, 1)
v_high = Triangular((2.5, 0), (3,1), (4, 1))
a_v_low = Adjective('v_low', v_low)
a_v_medium = Adjective('v_medium', v_medium)
a_v_high = Adjective('v_high', v_high)
visibility = Variable('visibility', 'km', a_v_low, a_v_medium, a_v_high)

# zmienna lingwistyczna `accident` opisująca jwysokość napiwku w skali od 0 do 25 procent (%)
# trzy wartości lingwistyczne,  zbiory rozmyte: `t_low`, `t_medium`, `t_high`


#                                           wypadek

a_very_low = Gaussian(0, 0.15, 1)
a_low = Gaussian(0.33, 0.2, 1)
a_medium = Gaussian(0.66, 0.2, 1)
a_high = Gaussian(1, 0.15, 1)

a_a_very_low = Adjective('a_very_low', a_very_low)
a_a_low = Adjective('a_low', a_low)
a_a_medium = Adjective('a_medium', a_medium)
a_a_high = Adjective('a_high', a_high)

accident = Variable('accident', '%', a_a_very_low, a_a_low, a_a_medium, a_a_high, defuzzification='COG', default=0)

x = np.linspace(10, 200, 1000)
x2 = np.linspace(0, 4, 1000)
x3 = np.linspace(0, 1, 1000)
fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(16, 9))
((ax1), (ax2), (ax3)) = axs
plot_fuzzyset(ax1, s_low, x, 'b', label='s_low')
plot_fuzzyset(ax1, s_medium, x, 'g', label='s_medium')
plot_fuzzyset(ax1, s_high, x, 'r', label='s_high')
plot_fuzzyset(ax1, s_very_high, x, 'black', label='s_very_high')

plot_fuzzyset(ax2, v_low, x2, 'b', label='v_low')
plot_fuzzyset(ax2, v_medium, x2, 'g', label='v_medium')
plot_fuzzyset(ax2, v_high, x2, 'r', label='v_high')

plot_fuzzyset(ax3, a_very_low, x3, 'violet', label='a_very_low')
plot_fuzzyset(ax3, a_low, x3, 'b', label='a_low')
plot_fuzzyset(ax3, a_medium, x3, 'g', label='a_medium')
plot_fuzzyset(ax3, a_high, x3, 'r', label='a_high')

plt.show()

from fuzzython.ruleblock import RuleBlock

scope = locals()
# speed: a_s_low,a_s_medium,a_s_high,a_s_very_high
# visibility: a_v_low,a_v_medium,a_v_high
# accident a_a_very_low, a_a_low, a_a_medium, a_a_high

rule1 = 'if speed is a_s_low and visibility is a_v_high then accident is a_a_very_low'
rule2 = 'if speed is a_s_low and visibility is a_v_medium then accident is a_a_very_low'
rule3 = 'if speed is a_s_low and visibility is a_v_low then accident is a_a_low'
rule4 = 'if speed is a_s_medium and visibility is a_v_high then accident is a_a_low'
rule5 = 'if speed is a_s_medium and visibility is a_v_medium then accident is a_a_medium'
rule6 = 'if speed is a_s_medium and visibility is a_v_low then accident is a_a_medium'
rule7 = 'if speed is a_s_high and visibility is a_v_high then accident is a_a_medium'
rule8 = 'if speed is a_s_high and visibility is a_v_medium then accident is a_a_high'
rule9 = 'if speed is a_s_high and visibility is a_v_low then accident is a_a_high'
rule10 = 'if speed is a_s_very_high and visibility is a_v_high then accident is a_a_medium'
rule11 = 'if speed is a_s_very_high and visibility is a_v_medium then accident is a_a_high'
rule12 = 'if speed is a_s_very_high and visibility is a_v_low then accident is a_a_high'


# # operators - operatory dla przecięcia, sumy i dopełnienia zbiorów rozmytych
# # activation - operator dla implikacji
# # accumulation - aperator dla agregacji reguł
block = RuleBlock('rb_mamdani', operators=('MIN', 'MAX', 'ZADEH'), activation='MIN', accumulation='MAX')
block.add_rules(rule1, rule2, rule3,rule4,rule5,rule7,rule8,rule9,rule10,rule11, scope=scope)

from fuzzython.systems.mamdani import MamdaniSystem

mamdani = MamdaniSystem('mamdani_model', block)



from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting

# przygotowanie siatki
sampledX = np.linspace(10, 200, 50)
sampledY = np.linspace(0.05, 4, 50)
x, y = np.meshgrid(sampledX, sampledY)
z = np.zeros((len(sampledX), len(sampledY)))

for i in range(len(sampledX)):
    for j in range(len(sampledY)):
        inputs = {'speed': x[i, j], 'visibility': y[i, j]}
        res = mamdani.compute(inputs)
        z[i, j] = res['rb_mamdani']['accident']

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis', linewidth=0.4, antialiased=True)
cset = ax.contourf(x, y, z, zdir='z', offset=-1, cmap='viridis', alpha=0.5)
cset = ax.contourf(x, y, z, zdir='x', offset=11, cmap='viridis', alpha=0.5)
cset = ax.contourf(x, y, z, zdir='y', offset=11, cmap='viridis', alpha=0.5)
ax.set_xlabel('speed')
ax.set_ylabel('visibility')
ax.set_zlabel('accident')
ax.view_init(30, 200)
plt.show()
