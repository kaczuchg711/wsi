import pymc3 as pm
from matplotlib import pyplot as plt
# pojawiającym komunikatem o theano nie trzeba się przejmować

with pm.Model() as grypa_model:
    # zmienna grypa o rozkładzie Bernoulliego z prawd. 0.1,
    # z prawd. 0.1 True (grypa), z prawd. 0.9 False (nie grypa)
    grypa = pm.Bernoulli('grypa', 0.1)

    # prawd. kataru pod warunkiem grypy
    # jeżeli grypa to p_katar=0.5, jeżeli nie grypa to p_katar=0.3
    p_katar = pm.Deterministic('p_katar', pm.math.switch(grypa, 0.5, 0.3))
    # zmienna katar o rozkładie Bernoulliego
    katar = pm.Bernoulli('katar', p_katar)

    # prawd. kaszlu pod warunkiem grypy
    # jeżeli grypa to p_kaszel=0.3, jeżeli nie grypa to p_kaszel=0.3
    p_kaszel = pm.Deterministic('p_kaszel', pm.math.switch(grypa, 0.3, 0.3))
    # zmienna kaszel o rozkładie Bernoulliego
    kaszel = pm.Bernoulli('kaszel', p_kaszel)

    # prawd. goraczki pod warunkiem grypy
    # jeżeli grypa to p_goraczka=0.8, jeżeli nie grypa to p_goraczka=0.4
    p_goraczka = pm.Deterministic('p_goraczka', pm.math.switch(grypa, 0.8, 0.4))
    goraczka = pm.Bernoulli('goraczka', p_goraczka)

with grypa_model:
    trace = pm.sample(1000, chains=1)  #liczba symulacji, są inne parametry warto sprawdzić w dokumentacji
trace

# zdefiniowane zmienne w naszym modelu
trace.varnames

# wygenerowana ścieżka dla zmiennej grypa
trace.get_values('grypa') # zwaraca obiekt ndarray

# w module pymc3 dostępne są metody do wygernerowania różnego rodzaju wykresów np.
axs = pm.traceplot(trace, varnames=['grypa', 'katar', 'kaszel', 'goraczka'])

# bezwarunkowe prawd. grypy (z założenia powinno być 0.1)
p_grypa = trace['grypa'].sum()/len(trace['grypa'])
print('p_grypa:', p_grypa)

# bezwarunkowe prawd. kataru (0.32)
p_katar = trace['katar'].sum()/len(trace['katar'])
print('p_katar', p_katar)

# bezwarunkowe prawd. kaszlu (0.3)
p_kaszel = trace['kaszel'].sum()/len(trace['kaszel'])
print('p_kaszel', p_kaszel)

# bezwarunkowe prawd. goraczki (0.44)
p_goraczka = trace['goraczka'].sum()/len(trace['goraczka'])
print('p_goraczka', p_goraczka)

# prawd. grypy pod warunkiem wystąpienia kataru (0.15625)
p_grypa_katar = (trace['grypa']*trace['katar']).sum()/trace['katar'].sum()
print('p_grypa_katar:', p_grypa_katar)

# prawd. grypy pod warunkiem wystąpienia kaszlu (0.1)
p_grypa_kaszel = (trace['grypa']*trace['kaszel']).sum()/trace['kaszel'].sum()
print('p_grypa_kaszel:', p_grypa_kaszel)

# prawd. grypy pod warunkiem wystąpienia goraczki (0.18182)
p_grypa_goraczka = (trace['grypa']*trace['goraczka']).sum()/trace['goraczka'].sum()
print('p_grypa_goraczka:', p_grypa_goraczka)

# prawd. grypy pod warunkiem wystąpienia kataru i goraczki (0.284(09))
p_grypa_katar_goraczka = (trace['grypa']*trace['katar']*trace['goraczka']).sum()/(trace['katar']*trace['goraczka']).sum()
print('p_grypa_katar_goraczka:', p_grypa_katar_goraczka)