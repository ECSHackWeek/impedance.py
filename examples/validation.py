import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('../')

from impedance import validation  # noqa E402

data = np.genfromtxt('./data/exampleData.csv', delimiter=',')
f = data[:, 0]
Z = data[:, 1] + 1j*data[:, 2]

mask = np.imag(Z) < 0

model_list, error_list = validation.measurementModel(f, Z, max_k=25)

fig = plt.figure()
plt.plot(Z.real, -Z.imag, 'o')
for model in model_list:
    Z_fit = model.predict(f)
    plt.plot(Z_fit.real, -Z_fit.imag)

fig2, ax2 = plt.subplots()
ax2.plot(range(1, len(error_list)+1), error_list)
ax2.set_yscale('log')
ax2.set_ylabel('Root Mean Squared Error')
ax2.set_xlabel('Number of RC elements')

plt.show()
