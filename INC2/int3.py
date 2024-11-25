import numpy as np
import matplotlib.pyplot as plt
import utils as utils
import pandas as pd
from scipy.optimize import curve_fit

def f(x,y,z,u,w):
    return np.sqrt(6-x**2-y**2-z**2-u**2-w**2)

def fit_model(n, a):
    return a / np.sqrt(n)

borders = [[0,7/10], [0, 4/5], [0, 9/10], [0, 1], [0, 11/10]]

n_values = [1000,2000, 3000,5000,10000,20000,30000,40000,50000, 70000, 80000, 100000, 200000]
d_values = np.arange(len(borders))+1
m = 100

int1 = utils.MultidimensionalIntegral(f,borders)

int_values = {}
std_values = {}
for d in d_values:
    int_array = []
    std_array = []
    print('\n')
    print(f'For {d} dimensions: \n')
    for n in n_values:
        mean_integral, std_integral, std_m_integral, _ = int1.md_sampling_method(n,d, m = m)
        print(f'For {n} iterations: mean_value = ', mean_integral, 'std:', std_integral, 'std_m:', std_m_integral)
        int_array.append(mean_integral)
        std_array.append(std_integral)
    int_values[d] = int_array
    std_values[d] = std_array




plt.figure(figsize=(10, 6))
colors = ['orangered','orange','yellowgreen','cornflowerblue','blueviolet']  # Paleta de colores
fit_results = {}

for i, d in enumerate(d_values):
    n_array = np.array(n_values)
    std_array = np.array(std_values[d])

    # Ajustar la curva
    popt, pcov = curve_fit(fit_model, n_array, std_array)
    a_fit = popt[0]
    fit_results[d] = a_fit

    # Graficar los datos y la curva ajustada
    plt.plot(n_array, std_array, 'o', color=colors[i], label=f'd = {d} ')
    plt.plot(n_array, fit_model(n_array, a_fit), '-', color=colors[i])

plt.xscale('log')
plt.yscale('log')
plt.xlabel('Number of Iterations (n)')
plt.ylabel(r'$\sigma$')
#plt.title('Error vs Number of Iterations for Different Dimensions')
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.savefig('results/dimensions_comparation.png')
plt.show()

print("Fit coefficients (a) for each dimension:")
for d, a in fit_results.items():
    print(f"Dimension {d}: a = {a:.3f}")
