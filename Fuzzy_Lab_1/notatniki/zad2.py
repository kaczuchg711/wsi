# zad2
import numpy as np
import matplotlib.pyplot as plt


def plot_fuzzyset(ax, fuzzy_set, x, *args, **kwargs):
    y = np.array([fuzzy_set(e) for e in x])
    ax.plot(x, y, *args, **kwargs)
    ax.set_ylim(-0.1, 1.1)
    ax.legend()


from fuzzython.variable import Variable
from fuzzython.adjective import Adjective
from fuzzython.fsets.triangular import Triangular


# zmienna lingwistyczna `price yesterday` opisująca cenę akcji wczoraj  od 1 do 20 zł
#                                 yesterday

y_low = Triangular((-0.1, 1), (0, 1), (10, 0))
y_middle = Triangular((5, 0), (10, 1), (15, 0))
y_high = Triangular((10, 0), (20, 1), (21, 1))

a_y_low = Adjective('y_low', y_low)
a_y_middle = Adjective('y_middle', y_middle)
a_y_high = Adjective('y_high', y_high)

price_yesterday = Variable('price_yesterday', 'zl', a_y_low, a_y_middle, a_y_high, defuzzification='COG', default=0)

# zmienna lingwistyczna `price today` opisująca cenę akcji dziś  od 1 do 20 zł
#                                       today

t_low = Triangular((-0.1, 1), (0, 1), (10, 0))
t_middle = Triangular((5, 0), (10, 1), (15, 0))
t_high = Triangular((10, 0), (20, 1), (21, 1))

a_t_low = Adjective('t_low', t_low)
a_t_middle = Adjective('t_middle', t_middle)
a_t_high = Adjective('t_high', t_high)

price_today = Variable('price_today', 'zl', a_t_low, a_t_middle, a_t_high, defuzzification='COG', default=0)

x = np.linspace(0, 20, 1000)
fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(8, 4.5))
((ax1), (ax2)) = axs
plot_fuzzyset(ax1, y_low, x, 'r', label='y_low')
plot_fuzzyset(ax1, y_middle, x, 'g', label='y_middle')
plot_fuzzyset(ax1, y_high, x, 'b', label='y_high')
plot_fuzzyset(ax2, t_low, x, 'r', label='t_low')
plot_fuzzyset(ax2, t_middle, x, 'g', label='t_middle')
plot_fuzzyset(ax2, t_high, x, 'b', label='t_high')
# plt.show()

rule1 = 'if price_yesterday is a_y_low      and price_today is a_t_low      then  z = price_today*0.5 + price_yesterday*0.5 '#
rule2 = 'if price_yesterday is a_y_low      and price_today is a_t_middle   then  z = price_today*0.8 + price_yesterday*0.4 '#1.2
rule3 = 'if price_yesterday is a_y_low      and price_today is a_t_high     then  z = price_today*1 + price_yesterday*1 '#1.4
rule4 = 'if price_yesterday is a_y_middle   and price_today is a_t_low      then  z = price_today*0.7 + price_yesterday*0.1 '#0.8
rule5 = 'if price_yesterday is a_y_middle   and price_today is a_t_middle   then  z = price_today*0.5 + price_yesterday*0.5'#
rule6 = 'if price_yesterday is a_y_middle   and price_today is a_t_high     then  z = price_today*1 + price_yesterday*0.1 '#1.1
rule7 = 'if price_yesterday is a_y_high     and price_today is a_t_low      then  z = price_today*0.6 + price_yesterday*0.1 '#0.7
rule8 = 'if price_yesterday is a_y_high     and price_today is a_t_middle   then  z = price_today*0.7 + price_yesterday*0.2 '#0.9
rule9 = 'if price_yesterday is a_y_high     and price_today is a_t_high     then  z = price_today*0.5 + price_yesterday*0.5'#

from fuzzython.ruleblock import RuleBlock

scope = locals()
block = RuleBlock('rb_takagi', operators=('MIN', 'MAX', 'ZADEH'), activation='MIN', accumulation='MAX')
block.add_rules(rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, scope=scope)

from fuzzython.systems.sugeno import SugenoSystem

sugeno = SugenoSystem('model_takagi', block)

inputs = {'price_yesterday': 2, 'price_today': 10}
res = sugeno.compute(inputs)
from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting

# przygotowanie siatki
sampled = np.linspace(0, 20, 50)
x, y = np.meshgrid(sampled, sampled)
z = np.zeros((len(sampled), len(sampled)))

for i in range(len(sampled)):
    for j in range(len(sampled)):
        inputs = {'price_yesterday': x[i, j], 'price_today': y[i, j]}
        res = sugeno.compute(inputs)
        z[i, j] = res['rb_takagi']

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis', linewidth=1, antialiased=True)
cset = ax.contourf(x, y, z, zdir='z', offset=-1, cmap='viridis', alpha=0.1)
cset = ax.contourf(x, y, z, zdir='x', offset=11, cmap='viridis', alpha=0.1)
cset = ax.contourf(x, y, z, zdir='y', offset=11, cmap='viridis', alpha=0.1)
ax.set_xlabel('price yesterday')
ax.set_ylabel('price today')
ax.set_zlabel('price tomorrow')
ax.view_init(30, 225)
plt.show()
