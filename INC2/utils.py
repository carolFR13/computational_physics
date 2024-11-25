import numpy as np
import random
import time


def std(x):
    x = np.array(x)
    return np.sqrt(np.mean(x**2)-np.mean(x)**2)

def std_m(x):
    m = len(x)
    x = np.array(x)
    return np.sqrt((1/m)*sum((x-np.mean(x))**2))

class Integral():
    '''
    class to compute definite integrals
    '''
    
    def __init__(self, function, a, b):
        self.function = function
        self.a = a
        self.b = b
        return None
    

    def simpson(self, inter):
        ''' Method to compute the integral of f from a to b
        using composite Simpson's method'''

        if inter % 2:
            raise ValueError("n must be even (received n=%d)" % inter)

        h = (self.b - self.a) / inter
        s = self.function(self.a) + self.function(self.b)

        for i in range(1, inter, 2):
            s += 4 * self.function(self.a + i * h)
        for i in range(2, inter-1, 2):
            s += 2 * self.function(self.a + i * h)

        return s * h / 3



    def sampling_method(self, inter): #metodo muestreo
        max_f = max(self.function(np.linspace(self.a, self.b, 1000)))
        ns = 0
        for _ in range(inter):
            x = self.a + (self.b-self.a) * random.random()
            y = max_f * random.random()
            fx = self.function(x)
            if y<fx:
                ns+=1
        F = max_f * (self.b-self.a) * ns/inter
        return F

    def mean_value_method(self, inter): #metodo th valor medio
        total_area = 0
        for _ in range(inter):
            x = self.a + (self.b - self.a) * random.random()
            total_area += self.function(x)
        F = (self.b-self.a)* (1/inter)*total_area
        return F
    

    def compute_integrals(self, n_values, m_values, analytical_sol):
        '''
        method to compute integrals with simpson, sampling and mean-value
        methods, computing the integral value, errors and standar deviations 
        with n iterations of the method, iterating m times to obtain the 
        standard deviation in MC methods

        :n_values: number of iterations in the method
        :m_vulues: number of times reitirating the computation 
        :analytical_sol: exact value of the integral
        '''

        total_results = {}
        total_times = {}

        for m in m_values:
            results = []
            times = {"n": [], "t_sampling": [], "t_mv": []}

            for n in n_values:

                simpson_result = self.simpson(n)
                error_simpson_values = abs(simpson_result - analytical_sol)

                 # computing m times the integral with sampling method for n interations 
                start_t = time.perf_counter()
                sampling_array = [self.sampling_method(n) for _ in range(m)]
                elapsed_time_samp = time.perf_counter() - start_t 
                
                # mean-value method
                start_t = time.perf_counter()
                mean_value_array = [self.mean_value_method(n) for _ in range(m)]
                elapsed_time_mv = time.perf_counter() - start_t

                # computing standard deviations
                std_samp_value = std(sampling_array)
                std_mv_value = std(mean_value_array)

                std_m_samp_value = std_m(sampling_array)
                std_m_mv_value = std_m(mean_value_array)

                # save results
                results.append({
                    "n": n,
                    "Simpson": simpson_result,
                    f"MC_Sampling_Mean_{m}": np.mean(sampling_array),
                    f"MC_Sampling_Std_{m}": std_samp_value,
                    f"MC_Sampling_Std_m_{m}": std_m_samp_value,
                    f"MC_Mean_Value_Mean_{m}": np.mean(mean_value_array),
                    f"MC_Mean_Value_Std_{m}": std_mv_value,
                    f"MC_Mean_Value_Std_m_{m}": std_m_mv_value,
                    "Error_Simpson": error_simpson_values,
                })

                times["n"].append(n)
                times["t_sampling"].append(elapsed_time_samp)
                times["t_mv"].append(elapsed_time_mv)


            total_results[m] = results
            total_times[m] = times
        return total_results, total_times


class MultidimensionalIntegral():

    def __init__(self, function, borders):
        self.function = function
        self.borders = borders
        self.max_dim = len(borders)
        return None
    
    def md_sampling_method(self, inter, d, m=1):
        '''
        Method to compute multidimensional integral using 
        the Monte Carlo sampling method up to dimension d<d_max

        :inter: number of iterations in each computation
        :d: number of dimensions

        '''

        if d > self.max_dim:
            raise ValueError("The number of dimensions cannot be bigger than the number of variables.")

        reduced_borders = self.borders[:d]

        def reduced_function(*args):
            # the dimensions not considered become 0
            full_args = list(args) + [0] * (self.max_dim - d)
            return self.function(*full_args)
        
        # d-dimensional space formed by the borders
        volume = np.prod([b[1] - b[0] for b in reduced_borders])

        # stimating maximum of the function in y coordenate
        samples = 1000000 # using large number because we are only computing it 1 time
        random_points = np.array([
            [b[0] + (b[1] - b[0]) * random.random() for b in reduced_borders]
            for _ in range(samples)
        ])
        max_f = max(reduced_function(*point) for point in random_points)

        integral_values = []

        # we compute the integral m times to obtain the standard deviation
        for _ in range(m):
            ns = 0
            for _ in range(inter):
                # random number in the domain
                random_point = [b[0] + (b[1] - b[0]) * random.random() for b in reduced_borders]
                # random number of y
                y = max_f * random.random()
                if y < reduced_function(*random_point):
                    ns += 1
            
            # value of the integral for that iteration 
            integral = volume * max_f * ns / inter
            integral_values.append(integral)
        
        mean_integral = np.mean(integral_values)
        std_integral = std(integral_values)
        std_m_integral = std_m(integral_values) # just to check it is the same value


        return mean_integral, std_integral, std_m_integral, integral
