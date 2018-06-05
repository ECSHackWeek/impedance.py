import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('../')

# import Randles circuit object
from impedance.circuits import Randles  # noqa E402

# read in data
data = np.genfromtxt('./data/exampleData.csv', delimiter=',')
f = data[:, 0]
Z = data[:, 1] + 1j*data[:, 2]

# initialize circuit objects
randles = Randles(initial_guess=[.01, .005, .1, .0001, 500])
randlesCPE = Randles(initial_guess=[.01, .005, .1, .9, .0001, 500], CPE=True)

# fit models
randles.fit(f, Z)
randlesCPE.fit(f, Z)

# print model objects
print(randles)
print(randlesCPE)

# impedance predictions based on model fits
Z_randles = randles.predict(f)
Z_randlesCPE = randlesCPE.predict(f)

# plot the data and the fits
fig, ax = plt.subplots(figsize=(5, 5))
ax.plot(np.real(Z), -np.imag(Z), 'o')
ax.plot(np.real(Z_randles), -np.imag(Z_randles),
        lw=3, label='Randles')
ax.plot(np.real(Z_randlesCPE), -np.imag(Z_randlesCPE),
        lw=3, label='Randles w/ CPE')
ax.set_aspect('equal')

# Set the labels to -imaginary vs real
ax.set_xlabel('$Z_{1}^{\prime}(\omega)$ $[\Omega]$', fontsize=20)
ax.set_ylabel('$-Z_{1}^{\prime\prime}(\omega)$ $[m\Omega]$', fontsize=20)

# Make the tick labels larger
ax.tick_params(axis='both', which='major', labelsize=14)

# Change the number of labels on each axis to five
ax.locator_params(axis='x', nbins=5, tight=True)
ax.locator_params(axis='y', nbins=5, tight=True)

# Add a light grid
ax.grid(b=True, which='major', axis='both', alpha=.5)
ax.legend(fontsize=18)

plt.tight_layout()
plt.show()
