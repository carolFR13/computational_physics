import numpy as np
import random
import matplotlib.pyplot as plt

'''
code to implement demon algorithm for microcanonical ensemble (NVE)
'''

plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'


N_tot = 10000 # number of particles
m = 1 # mass for each particle
v = np.ones(N_tot)*2

E_0 = sum((1/2)*m*v**2) # fixed energy
E_demon = 0
steps = 1000000
count = 0
demon_energy = []

for i in range(steps):
    rd = random.randint(0,N_tot-1)
    delta_v = random.uniform(-1,1)
    delta_E = (1/2) * m * ((v[rd] + delta_v)**2 - v[rd]**2)
    
    if delta_E <=0:
        v[rd] += delta_v  
        E_demon += abs(delta_E) 
        count += 1
    elif E_demon >= delta_E:  
        v[rd] += delta_v  
        E_demon -= delta_E 
        count += 1
    demon_energy.append(E_demon)


print('Total energy of the system:',E_0)
print('Final energy of the demon:', E_demon)
print('Number of times the demon interacts',count, 'out of', steps,'that is', count/steps*100, '%')


# ---------------------
# computing the theoretical maxwell-boltzmann distribution for velocities (k_b =1)
T_mean = np.mean(v**2)

def maxwell_boltzmann(v, T, m=1):
    return np.sqrt(m / (2 * np.pi * T)) * np.exp(-m * v**2 / (2 * T))

v_values = np.linspace(min(v), max(v), 500)
mb_distribution = maxwell_boltzmann(v_values, T_mean)

plt.hist(demon_energy, bins = 20, alpha=0.65, color = 'blue', edgecolor = 'black', label = 'Experimental values')
plt.xlabel('\# iterations')
plt.ylabel(r'$E_{demon}$')
plt.savefig('E_demon.png')
plt.show()


plt.hist(v, bins = 27, alpha=0.65, density= True, color = 'blue', edgecolor = 'black', label = 'Experimental values')
plt.plot(v_values, mb_distribution, color='black', linewidth=1, label='Maxwell-Boltzmann distribution')
plt.xlabel('v')
plt.ylabel('Probability density')
plt.legend()
plt.savefig('v_distr.png')
plt.show()



