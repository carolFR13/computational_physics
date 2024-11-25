import utils as utils
import numpy as np
import matplotlib.pyplot as plt
import time


# changing graphs style
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'

rw = utils.RandomWalk((10, 20, 30), 100)
division = 8 # number of division for each cm

# start = time.perf_counter()
# pot_python = rw.compute_potential(division, iterations=50)  # Versión secuencial
# elapsed_time = time.perf_counter() - start

# print('With normal python the computation takes', elapsed_time, 's')

start = time.perf_counter()
pot_numba = rw.compute_potential_numba(division, iterations = 300)  # Versión acelerada con numba
elapsed_time = time.perf_counter() - start

print('With numba the computation takes', elapsed_time, 's')


# coordinates of the space
nx, ny, nz = pot_numba.shape

x = np.linspace(0, rw.x_lim, nx)
y = np.linspace(0, rw.y_lim, ny)
z = np.linspace(0, rw.z_lim, nz)

# graphs of the result

# **planes in z = 2, z = z_max/2, z = z_max - 2**
planes_z = [int(2 * division), nz // 2, int((rw.z_lim - 2) * division)]


for i, z_idx in enumerate(planes_z):
    pot_horizontal = pot_numba[:, :, z_idx]  # plane in z = cte

    plt.figure()
    plt.xlabel("x (cm)")
    plt.ylabel("y (cm)")
    plt.title(f"z = {z[z_idx]:.2f} cm")
    plt.imshow(pot_horizontal.T, extent=(0, rw.x_lim, 0, rw.y_lim), origin='lower', cmap='viridis')
    plt.colorbar(label="Potential (V)")
    plt.savefig(f'results/plane_z_{i}.png')
    plt.show()

# **planes in x = 1, x = x_max/2, x = x_max - 1**
planes_x = [int(1 * division), nx // 2, int((rw.x_lim - 1) * division)]

for i,x_idx in enumerate(planes_x):
    pot_vertical = pot_numba[x_idx, :, :]  # plane in x = cte

    plt.figure()
    plt.xlabel("y (cm)")
    plt.ylabel("z (cm)")
    plt.title(f"x = {x[x_idx]:.2f} cm")
    plt.imshow(pot_vertical.T, extent=(0, rw.y_lim, 0, rw.z_lim), origin='lower', cmap='viridis')
    plt.colorbar(label="Potential (V)")
    plt.savefig(f'results/plane_x_{i}.png')
    plt.show()

# **horizontal plane: z = z_max / 2**
z_idx = nz // 2
pot_horizontal = pot_numba[:, :, z_idx]  

x_mesh, y_mesh = np.meshgrid(x, y, indexing='ij')

print("x_mesh shape:", x_mesh.shape)
print("y_mesh shape:", y_mesh.shape)
print("pot_horizontal shape:", pot_horizontal.shape)


fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x_mesh, y_mesh, pot_horizontal, cmap='viridis', edgecolor='none')

ax.set_xlabel("x (cm)")
ax.set_ylabel("y (cm)")
ax.set_zlabel("Potential (V)")
ax.set_title(f"z = {z[z_idx]:.2f} cm")
plt.savefig(f'results/surface_z.png')
plt.show()

# **vertical plane: x = x_max / 2**
x_idx = nx // 2

pot_vertical = pot_numba[x_idx, :, :] 

y_mesh, z_mesh = np.meshgrid(y, z, indexing='ij')

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(y_mesh, z_mesh, pot_vertical, cmap='viridis', edgecolor='none')

ax.set_title(f"x = {x[x_idx]:.2f} cm")
ax.set_xlabel("y (cm)")
ax.set_ylabel("z (cm)")
ax.set_zlabel("Potencial (V)")
plt.savefig(f'results/surface_x.png')
plt.show()
