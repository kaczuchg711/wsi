import pymc3 as pm
import numpy as np

# szukamy
# P(H1 | E1)
# P(H1 | (E2 & E3))
# P(H1 | (E1 & E4 & E5))

with pm.Model() as zabojstwo_model:
    # zminna zabojstwo
    h1 = pm.Bernoulli('h1', 0.5)

    # prawd. znalezienia odciskow pod warunkiem zabojstwa
    p_E1 = pm.Deterministic('p_E1', pm.math.switch(h1, 0.7, 0.3))
    E1 = pm.Bernoulli('E1', p_E1)

    # główny podejrzany nie ma alibi na czas popełnienia zabójstwa
    p_E2 = pm.Deterministic('p_E2', pm.math.switch(h1, 0.8, 0.4))
    E2 = pm.Bernoulli('E2', p_E2)

    #  główny podejrzany miał motyw zabicia ofiary,
    p_E3 = pm.Deterministic('p_E3', pm.math.switch(h1, 0.9, 0.5))
    E3 = pm.Bernoulli('E3', p_E3)

    # główny podejrzany był widziany w sądziedztwie miejsca,
    # w którym mieszka nielegalny handlarz bronią,
    p_E4 = pm.Deterministic('p_E4', pm.math.switch(h1, 0.4, 0.2))
    E4 = pm.Bernoulli('E4', p_E4)

    # świadek zbrodni podał rysopis zabójcy nie pasujący do głównego podejrzanego.
    p_E5 = pm.Deterministic('p_E5', pm.math.switch(h1, 0.2, 0.4))
    E5 = pm.Bernoulli('E5', p_E5)

with zabojstwo_model:
    trace = pm.sample(10000, chains=1)

# P(H1 | E1) Gdyby znaleziono na miejscu zbrodni jego odciski palców
p_zabojstwo_pw_odciski = (trace['h1'] * trace['E1']).sum() / trace['E1'].sum()
print('prawdopodobieństwo gdyby znaleziono na miejscu zbrodni jego odciski palców:', p_zabojstwo_pw_odciski)

# P(H1 | (E2 & E3)) Gdyby stwierdzono, że nie miał alibi i miał motyw.
p_zabojstwo_pw_alibi_motyw = (trace['h1'] * trace['E2'] * trace['E3']).sum() / (trace['E2'] * trace['E3']).sum()
print('prawdopodobieństwo gdyby stwierdzono, że nie miał alibi i miał motyw:', p_zabojstwo_pw_alibi_motyw)

# P(H1 | (E1 & E4 & E5)) #Gdyby znaleziono na miejscu zbrodni jego odciski palców oraz stwierdzono,
# że był widziany w sąsiedztwie miejsca, w którym mieszka nielegalny handlarz bronią,
# ale świadek zbrodni podał rysopis zabójcy nie pasujący do głównego podejrzanego.
p_zabojstwo_pw_odciski_handlarz_rysopis = (trace['h1'] * trace['E1'] * trace['E4']*trace['E5']).sum() / (trace['E2'] * trace['E4'] * trace['E5']).sum()
print('P(H1 | (E1 & E4 & E5)):', p_zabojstwo_pw_odciski_handlarz_rysopis)
