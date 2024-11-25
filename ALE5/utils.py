import random
import numpy as np
from numba import njit, prange



class RandomWalk:

    '''
    class to obtain the values of the potential in a box with dimiensions 
    x_lim x y_lim x z_lim and a fixed potential in the top and bottom sides
    - (x,y) planes for x = z_lim and z = 0.

    The box is placed from the point (0,0,0) to (x_lim,y_lim,z_lim)
    '''

    def __init__(self, dimensions, potential):

        # dimensions of the box
        self.x_lim, self.y_lim, self.z_lim = dimensions

        # potential for top and bottom sides
        self.potential = potential

        return None
    
    def check_point(self, point) : # not sure if this is the most eficiente way
        '''
        checking if a given point reached a wall of the box, if true returns the 
        value of the potential in that wall.
        '''
        xi, yi, zi = point

        if xi <= 0 or xi >= self.x_lim or yi <= 0 or yi >= self.y_lim:
            return True, 0  
        elif zi <= 0 or zi >= self.z_lim:  
            return True, self.potential
        else:
            return False, 0
    
    def random_walk(self, init_point, step_size):
        '''
        method to run the random_walk from an init point until 
        reaching a wall

        returns the final point and the potential in the final point
        '''    

        x, y, z = init_point

        while True:

            # generate random steps
            dx = step_size if random.random() < 0.5 else -step_size
            dy = step_size if random.random() < 0.5 else -step_size
            dz = step_size if random.random() < 0.5 else -step_size

            # update position
            x += dx
            y += dy
            z += dz

            finished, potential = self.check_point((x,y,z))
            if finished :
                break
        return potential

    def compute_potential(self, division, iterations=100):
        '''
        methood to cumpute the potentail in the given space with 
        the mentioned boundary conditions

        :division: number of divisions considered in each dimension
        for 1 unit of length (in this case cm) 
        (number of new intervals not number of cuts in the interval)
        :iterations: number of random walks performed to compute the potential
        in each point
        '''

        nx, ny, nz = (int(d * division) for d in (self.x_lim, self.y_lim, self.z_lim))

        final_pot = np.zeros((nx, ny, nz))


        step_size = 1/division

        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    pot = 0
                    # scale point to real coordenates since we are using steps with step_size 
                    x0, y0, z0 = i / division, j / division, k / division
                    for _ in range(iterations):
                        pot += self.random_walk((x0, y0, z0), step_size)
                        
                    
                    final_pot[i,j,k] = pot/iterations
        
        return final_pot

    def compute_potential_numba(self, division, iterations=100):
        '''
        same method as compute potential but optimized using numba
        '''

        nx, ny, nz = (int(d * division) for d in (self.x_lim, self.y_lim, self.z_lim))
        step_size = 1 / division


        # function to perform the random walk optimazed using numba
        @njit
        def random_walk_static(x, y, z, step_size, x_lim, y_lim, z_lim, potential):
            while True:
                # generate random steps
                dx = step_size if random.random() < 0.5 else -step_size
                dy = step_size if random.random() < 0.5 else -step_size
                dz = step_size if random.random() < 0.5 else -step_size

                # update position
                x += dx
                y += dy
                z += dz

                # check boundaries
                if x <= 0 or x >= x_lim or y <= 0 or y >= y_lim:
                    return 0
                elif z <= 0 or z >= z_lim:
                    return potential

        # function to compute potential in a point optimazed using numba
        @njit(parallel=True)
        def calculate_potential(nx, ny, nz, step_size, x_lim, y_lim, z_lim, potential, iterations):
            pot = np.zeros((nx, ny, nz))
            for i in prange(nx):
                for j in prange(ny):
                    for k in prange(nz):
                        x0, y0, z0 = i / division, j / division, k / division
                        avg_potential = 0
                        for _ in range(iterations):
                            avg_potential += random_walk_static(x0, y0, z0, step_size, x_lim, y_lim, z_lim, potential)
                        pot[i, j, k] = avg_potential / iterations
            return pot

        final_pot = calculate_potential(nx, ny, nz, step_size, self.x_lim, self.y_lim, self.z_lim, self.potential, iterations)
        
        return final_pot


