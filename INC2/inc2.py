import numpy as np
import matplotlib.pyplot as plt
import utils as utils
import pandas as pd
import os
from openpyxl import Workbook

# changing graphs style
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'

def f(x):
    return np.exp(-x) 

def std_mc(n):
    return 1/np.sqrt(n)

def error_simpson(n):
    return 1/n**4


# number of iterations for each simulation
n_values = [100, 200, 300, 500, 700, 1000, 3000, 5000, 7000, 10000, 15000, 30000, 50000, 70000, 100000, 200000, 400000, 600000, 1000000] 

a, b = 0, 1

analytical_sol = 1 - np.exp(-1)  # analytical solution for the integral


int1 = utils.Integral(f, a, b)

m_values = [100, 200]


# --------------------------------------------------
# computing the integrals for n_values interarions m_values times
# this takes time !!!



# results, times = int1.compute_integrals(n_values, m_values, analytical_sol)

# print("Contents of results:")
# print(results)
# print("Contents of times:")
# print(times)

# # printing results in dataframe

# if not os.path.exists("results"):
#     os.makedirs("results")

# # saving thte results in a file for later study without waiting the computational time
# with pd.ExcelWriter('results/results.xlsx') as writer:  
#     for m, results in results.items():
#         df_results = pd.DataFrame(results)
#         df_results.to_excel(writer, sheet_name=f"Results_m_{m}", index=False)

#     for m, times in times.items():
#         df_times = pd.DataFrame(times)
#         df_times.to_excel(writer, sheet_name=f"Times_m_{m}", index=False)


# ---------------------------------------------------------------
# reading the results to analice, once you generated the file

df_results1 = pd.read_excel('results/results.xlsx', sheet_name='Results_m_100')
df_results2 = pd.read_excel('results/results.xlsx', sheet_name='Results_m_200')
df_times1 = pd.read_excel('results/results.xlsx', sheet_name='Times_m_100')
df_times2 = pd.read_excel('results/results.xlsx', sheet_name='Times_m_200')



# ----------------------------------------------------------------
# plotting the results 


#plt.plot(n_values,np.array(df_times1["t_sampling"])/1000, marker='o', label = 'Sampling method for m = 100', color = 'cornflowerblue')
#plt.plot(n_values,np.array(df_times1["t_mv"]), marker='o', label = 'Mean value method  for m = 100', color = 'mediumseagreen')
plt.plot(n_values,np.array(df_times2["t_sampling"]), marker='o', label = 'Sampling method', color = 'cornflowerblue')
plt.plot(n_values,np.array(df_times2["t_mv"]), marker='o', label = 'Mean value method', color = 'mediumseagreen')

plt.ylabel(r't(s)')
plt.xlabel('Number of Iterations (n)')
plt.grid(alpha=0.3)
plt.legend()
plt.savefig('results/time_comparation_2.png')
plt.show()


# graph of integral results
plt.figure(figsize=(10, 6))
plt.errorbar(n_values, df_results2["MC_Sampling_Mean_200"], yerr=df_results2["MC_Sampling_Std_200"],capsize=3, label="Sampling method", fmt='o', color = 'cornflowerblue')
plt.errorbar(n_values, df_results2["MC_Mean_Value_Mean_200"], yerr=df_results2["MC_Mean_Value_Std_200"],capsize=3, label="Mean value method", fmt='o', color = 'mediumseagreen')
plt.errorbar(n_values, df_results2["Simpson"], yerr=df_results2["Error_Simpson"],capsize=3, label="Simpson", fmt='o', color = 'orange')
plt.axhline(analytical_sol, color='orangered', linestyle='--', label="Analytical Solution")
plt.grid(True, alpha = 0.5, which="both", linestyle='--', linewidth=0.5)
plt.xlabel("Number of Iterations (n)")
plt.ylabel("Integral Value")
plt.xscale('log')
#plt.yscale('log')
plt.legend()
plt.savefig('results/integral_values_2.png')
plt.show()


n_array = np.linspace(min(n_values), max(n_values), 100)

# graph of std results
plt.figure(figsize=(12, 8))
plt.plot(n_values,  df_results1["Error_Simpson"], label="Simpson error", marker='o', linestyle='-', color = 'orange')
plt.plot(n_array,  error_simpson(n_array), label=r"$n^{-4}$", linestyle=':', color = 'orangered')
plt.plot(n_values, df_results1["MC_Sampling_Std_100"], label="Sampling Standard Deviation for m = 100", marker='o', linestyle='--', color = 'cornflowerblue')
plt.plot(n_values, df_results2["MC_Sampling_Std_200"], label="Sampling Standard Deviation for m = 200", marker='o', linestyle='--', color = 'royalblue')
plt.plot(n_values, df_results1["MC_Mean_Value_Std_100"], label="Mean Value Standard Deviation for m = 100", marker='o', linestyle='-.', color = 'mediumseagreen')
plt.plot(n_values, df_results2["MC_Mean_Value_Std_200"], label="Mean Value Standard Deviation for m = 200", marker='o', linestyle='-.', color = 'forestgreen')
plt.plot(n_array,  std_mc(n_array), label=r"$n^{-1/2}$", linestyle=':', color = 'blueviolet')
plt.yscale('log')
plt.xscale('log')
plt.xlabel("Number of Iterations (n)", fontsize=12)
plt.ylabel("Error / Standard Deviation", fontsize=12)
plt.legend()
plt.grid(True, alpha = 0.5, which="both", linestyle='--', linewidth=0.5)
plt.savefig('results/std_values_2.png')
plt.show()
