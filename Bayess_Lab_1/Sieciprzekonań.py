# źródło:
# https://bugra.github.io/work/notes/2014-05-23/simple-bayesian-network-via-monte-carlo-markov-chain-mcmc-pymc/
# https://gist.github.com/cs224/9a19b4ba2c7511e317be90c32a4d40d7
import pymc3 as pm
import numpy as np


with pm.Model() as model:
    rain = pm.Bernoulli('rain', 0.2)
    sprinkler_p = pm.Deterministic('sprinkler_p', pm.math.switch(rain, 0.01, 0.40))
    sprinkler = pm.Bernoulli('sprinkler', sprinkler_p)
    grass_wet_p = pm.Deterministic('grass_wet_p', pm.math.switch(rain, pm.math.switch(sprinkler, 0.99, 0.80), pm.math.switch(sprinkler, 0.90, 0.0)))
    grass_wet = pm.Bernoulli('grass_wet', grass_wet_p)

    trace = pm.sample(20000, chains=1)

pm.traceplot(trace)

# Jakie jest prawdopodobieństwo, że podało jeśli wiadomo, że trawa jest mokra?
p_rain_wet = (trace['rain']*trace['grass_wet']).sum()/trace['grass_wet'].sum()
print('p_rain_wet:', p_rain_wet)

# Jakie jest prawdopodobieństwo, że włączył się spryskiwacz jeśli wiadomo, że trawa jest mokra?
p_sprinkler_wet = (trace['sprinkler']*trace['grass_wet']).sum()/trace['grass_wet'].sum()
print('p_sprinkler_wet:', p_sprinkler_wet)

# Jakie jest prawdopodobieństwo, że trawa jest mokra jeśli wiadomo, że spryskiwacz się nie włączył oraz nie padało?
p_not_sprinkler_rain_wet = (trace['grass_wet']*np.logical_not(trace['sprinkler'])*np.logical_not(trace['rain'])).sum()/(np.logical_not(trace['sprinkler'])*np.logical_not(trace['rain'])).sum()
print('p_not_sprinkler_rain_wet:', p_not_sprinkler_rain_wet)