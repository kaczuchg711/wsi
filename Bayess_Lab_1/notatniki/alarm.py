# System alarmowy w mieszkaniu, reaguje na włamania oraz, niestety, również na drobne trzęsienia (ziemi).
# Sąsiedzi John i Mary są umówieni, żeby zadzwonić do właściciela gdy usłyszą alarm.
# John jest nadgorliwy i bierze różne zdarzenia (np. dzwonek telefonu) za sygnał alarmowy (i wtedy zawsze dzwoni).
# Mary rozpoznaje alarm poprawnie, lecz często słucha głośnej muzyki i może go w ogóle nie usłyszeć.
#
# Jakie jest prawdopodobieństwo, że:
#
#     1.włączy się alarm?
#     2.doszło do włamanie jeśli wiadom, że włączył się alarm?
#     3.zdarzyło się trzęsienie ziemi jeśli wiadomo, żę włączył się alarm?
#     4.w razie włamania ktoś zadzwoni?
#     5.zawiadomienie o włamaniu jest fałszywe?
#     6.rozległ się alarm, przy czym nie wystąpiło ani trzęsienie ziemi ani włamanie, ale oboje John i Mary zadzwonili? (prawd. bezwarunkowe)
#
# 1 A-wlaczenie sie alarmu
# B-wlamanie
# 2 B|A
# E-trzesienie ziemi
# 3 E|A
# J-zadzwonil  John
# M-zadzwonila Marry
# 4 J+M|B
# 5 J+M|~B
# 6 mnozenie?

import pymc3 as pm
import numpy as np

with pm.Model() as model:
    B = pm.Bernoulli('B', 0.001)
    E = pm.Bernoulli('E', 0.002)

    p_A = pm.Deterministic('p_A', pm.math.switch(B,pm.math.switch(E,0.95,0.94),pm.math.switch(E,0.29,0.001)))
    A = pm.Bernoulli('A', p_A)

    p_J = pm.Deterministic('p_J', pm.math.switch(A, 0.9, 0.05))
    J = pm.Bernoulli('J',p_J)

    p_M = pm.Deterministic('p_M', pm.math.switch(A, 0.7, 0.01))
    M = pm.Bernoulli('M', p_M)

with model:
    trace = pm.sample(100000, chains=1)

p_A = trace['A'].sum()/len(trace['A'])
print('włączy się alarm:', p_A)

p_BwA = (trace['B'] * trace['A']).sum() / trace['A'].sum()
print('doszło do włamanie jeśli wiadomo, że włączył się alarm:', p_BwA)

p_EwA = (trace['E'] * trace['A']).sum() / trace['A'].sum()
print('doszło do włamanie jeśli wiadomo, że włączył się alarm:', p_EwA)

p_JM_B = (trace['B'] * trace['J']).sum()/(trace['B']).sum() + (trace['B'] * trace['M']).sum()/(trace['B']).sum() - (trace['B'] * trace['M'] * trace['J']).sum()/(trace['B']).sum()
print('w razie włamania ktoś zadzwoni:', p_JM_B)

p_JM_nB = ((1 - trace['B']) * trace['J']).sum()/((1 - trace['B'])).sum() + ((1 - trace['B']) * trace['M']).sum()/((1 - trace['B'])).sum() - ((1 - trace['B']) * trace['M'] * trace['J']).sum()/((1 - trace['B'])).sum()
print('ktoś zadzwoni a nie było włamania:', p_JM_nB)

p_E = trace['E'].sum()/len(trace['E'])
p_B = trace['B'].sum()/len(trace['B'])
p_J = trace['J'].sum()/len(trace['J'])
p_M = trace['M'].sum()/len(trace['M'])

p_6 = p_A * (1 - p_E) * (1 - p_B) * p_J * p_M
print("zad6:",p_6)