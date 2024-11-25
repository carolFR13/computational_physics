import numpy as np
import random
import matplotlib.pyplot as plt

'''
we want to generate the variables theta and phi with 
a distribution such that the resulting plot in 3d is an sphere,
that is, we will have an uniform distribution in phi between 0 and 2pi
and a sin(theta) distribution for theta between 0 and pi

we will try to implement the truncate method
'''

# Changing graphs style
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'

# probability function of theta varibale
# function already normalized (max value = 1)
def p(theta):
    return np.sin(theta)



n = 10000  #number of points 
phi = [random.uniform(0, 2*np.pi) for i in range(n)]


theta = []
while True:
    rd_1 = random.uniform(0, np.pi)
    p_1 = p(rd_1)
    rd_2 = random.random()
    if rd_2<p_1:
        theta.append(rd_1)
    if len(theta)==n:
        break



plt.hist(theta, bins=30, density=True, alpha=0.5)
plt.xlabel(r'$\theta$')
plt.ylabel(r'p($\theta$)')
plt.show()


plt.hist(phi, bins=30, density=True, alpha=0.5)
plt.xlabel(r'$\phi$')
plt.ylabel(r'p($\phi$)')
plt.show()


r = 1 ; phi = np.array(phi) ; theta = np.array(theta)

x = r * np.sin(theta) * np.cos(phi)
y = r * np.sin(theta) * np.sin(phi)
z = r * np.cos(theta)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(projection='3d')
ax.scatter(x, y, z, s=0.1, color='b', alpha=0.5)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

plt.show()