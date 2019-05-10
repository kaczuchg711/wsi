##### Przykład: Model Takagi-Sugeno: Decydujemy o wysokości napiwku
import numpy as np
import matplotlib.pyplot as plt
from fuzzython.ruleblock import RuleBlock

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


rule4 = 'if quality is a_q_poor or service is a_s_poor then z=quality*0.5+service*0.5'
rule5 = 'if quality is a_q_average then z=quality*0.7+5'
rule6 = 'if quality is a_q_good or service is a_s_good then z=quality*0.4+service*0.6+15'


scope = locals()
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

plt.show()