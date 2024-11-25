import numpy as np
import random
import time
from scipy.special import gamma
from scipy.stats import chi2
import scipy.integrate as sci

def constant(x, a):
            return a * np.ones_like(x)

def exponential(x, mu):
    return  np.exp(-x/mu)

def gaussian(x,mu,sigma):
    return  1/np.sqrt(2*np.pi) /sigma * np.exp(-(x-mu)**2/2/sigma/sigma)



class Read():
    '''
    class to read files, implementing a method to optimice reading 
    large files
    '''

    def __init__(self, file_name) -> None:
        '''
        :file_name: path of the file 
        '''
        self.file_name = file_name
        return None

    def read_large_file(self, block_size : int = 1024*8):
        '''
        reading generator optimiced for reading large files.

        :bllock_size: size in bytes
        '''
        with open(self.file_name, 'r') as file:
            while True:
                # Leer un bloque de números
                block = file.readlines(block_size)
                if not block:
                    break  # Salir si no hay más datos

                block = np.array(list(map(int, block)), dtype=np.int64)
                
                yield block  # Devuelves el bloque para procesarlo más tarde

    def read_file(self, header : bool = False) -> np.ndarray:
        '''
        reading method that reads the file as a whole.
        '''
        if header:
            data = np.loadtxt(self.file_name, skiprows=1)
        else:
            data = np.loadtxt(self.file_name, dtype=np.uint32)
        return np.transpose(data)

class Statistics():

    def __init__(self, data) -> None:
        self.data = np.array(data)
        return None
    
    def mean(self) -> float:
        return sum(self.data)/len(self.data)
    
    def std(self) -> np.float64:
        return (sum((x - self.mean())**2 for x in self.data)/len(self.data))**0.5
    
    def analysis_uniform_distribution(self):
        '''
        method to analyse if the distribution of permutations is uniform

        the distribution is given by 120 points with value = number of counts 
        of that given permutation
        '''

        num_permutations = len(self.data)
        expected_value =  np.sum(self.data) / num_permutations


        chi_squared = np.sum((self.data - expected_value)**2 / expected_value)
        dof = len(self.data) - 1

        p_value = 1 - chi2.cdf(chi_squared, dof)

        print('Expected value:', expected_value,'+-', np.sqrt(expected_value) )

        print(f"Chi-squared: {chi_squared:.2f}")
        print(f"Degrees of freedom: {dof}")
        print(f"P-value: {p_value:.4f}")   

        return expected_value, np.sqrt(expected_value)
        

    def analysis_diff(self, n_bins):

        hist_counts, bin_edges = np.histogram(self.data, bins=n_bins)
        bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
        bin_width = bin_edges[1] - bin_edges[0]  # Suponemos bins de igual tamaño
        
        mu = np.mean(self.data)

        expected_values = exponential(bin_centers, mu)
    
        valid_bins = (hist_counts > 5)

        filtered_counts = hist_counts[valid_bins]
        filtered_exp = expected_values[valid_bins]
        filtered_centers = bin_centers[valid_bins]
        filtered_edges = bin_edges[:-1][valid_bins]

        area_total = np.sum(filtered_counts) * bin_width
        normalized_counts = filtered_counts / area_total

        # Calcular chi-cuadrado
        chi_squared = np.sum((normalized_counts - filtered_exp) ** 2 / filtered_exp)
        dof = len(filtered_exp) - 1
        p_value = 1 - chi2.cdf(chi_squared, dof)

        yerr = np.sqrt(normalized_counts) 

        # Resultados
        print(f"mu: {mu:.8f}")
        print(f"Chi-squared: {chi_squared:.2f}")
        print(f"Degrees of freedom: {dof}")
        print(f"P-value: {p_value:.4f}")

        return normalized_counts, filtered_edges, filtered_centers, bin_width, mu, yerr

    def analysis_sums(self, n_bins):

        filtered_data = self.data[(self.data >= 40) & (self.data <= 60)]


        hist_counts, bin_edges = np.histogram(filtered_data, bins=n_bins, density=False)
        

        print(hist_counts)
        bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
        bin_width = bin_edges[1] - bin_edges[0]


        mu = np.mean(filtered_data)
        sigma = np.std(filtered_data)
        
        expected_values = gaussian(bin_centers, mu, sigma)

        # Normalizar los valores esperados al área del histograma
 
        
        valid_bins = (hist_counts > 10) & (expected_values > 1e-6)

        filtered_counts = hist_counts[valid_bins]
        filtered_exp = expected_values[valid_bins]
        filtered_centers = bin_centers[valid_bins]

        area_total = np.sum(filtered_counts) * bin_width
        normalized_counts = filtered_counts / area_total

        area_total_exp = np.sum(filtered_exp) * bin_width
        filtered_exp *= np.sum(filtered_counts) / area_total_exp



        chi_squared = np.sum((filtered_counts - filtered_exp) ** 2 / filtered_exp)
        dof = len(filtered_exp) - 2  # Restamos 2 por los parámetros ajustados (mu y sigma)
        p_value = 1 - chi2.cdf(chi_squared, dof)
        
        # Paso 5: Imprimir resultados
        print(f"Media (mu): {mu:.8f}")
        print(f"Desviación estándar (sigma): {sigma:.8f}")
        print(f"Chi-cuadrado: {chi_squared:.2f}")
        print(f"Grados de libertad: {dof}")
        print(f"P-valor: {p_value:.4f}")
        
        # Errores del histograma
        yerr = np.sqrt(hist_counts[valid_bins]) / area_total

        return normalized_counts, filtered_centers, bin_width, mu, sigma, yerr


class Diehard_tests():

    def __init__(self, file_name: str) -> None:
        '''
        :file_name: path of the file containing the random numbers
        '''
        self.file_name = file_name
        return None
    
    def birthday_spacing(self, n: int = 100) -> tuple[list, float]:
        '''
        method to obtaing the resulting histogram of performing 
        birthday spacing test to a bunch of random numbers

        :file_name: path to file with the random numbers
        :n: number of points selected in eack block of data 
            (see read_large_file method)
        '''
        # each block contains around 762 numbers for mt file
        iterator = Read(self.file_name).read_large_file() 
        

        all_diff = []
        start_time = time.time()
        for block in iterator:
            if len(block) < n:
                continue

            rd_points = random.sample(list(block), n) 
            rd_points.sort()
            diff = np.diff(rd_points)
            all_diff.extend(diff)

        end_time = time.time()
        elapsed_time = end_time - start_time

        return all_diff, elapsed_time
    
    def overlapping_permutations(self) -> tuple[list, float]:
        '''
        method to obtaing the number of times each permutation 
        appears when coosing 5 consecutive numbers, that is,
        the returned list will have 5! = 120 elements with the 
        counts for each permutation.
        '''

        iterator = Read(self.file_name).read_large_file()
        dist = {} ; hist = []
        leftover = np.array([])

        start_time = time.time()
        for block in iterator:
            #print(block, type(block))
            block = np.concatenate((leftover, block))
            for i in range(0,len(block),5):
                xi = block[i:i+5]
                if len(xi)<5: 
                    leftover = xi
                    break
                args = np.argsort(xi)
                key = str(args)
                if key not in dist:
                    dist[key] = 1
                else:
                    dist[key] += 1

        end_time = time.time()
        elapsed_time = end_time - start_time
        hist = list(dist.values())
        return hist, elapsed_time
    
    def overlapping_sum(self, period: float) -> tuple[list, float]:
        '''
        method to compute the sum of 100 consecutive numbers, 
        the result is an array with the values of the sum.

        the random numbers need to be normalized between 0 and 1
        :period: max value possible of the random numbers

        '''
         # normalized numbers !! 
        iterator = Read(self.file_name).read_large_file() 

        sums = []
        leftover = np.array([])
        start_time = time.time()
        for block in iterator:
            #print(block, type(block))
            block = np.concatenate((leftover, block))
            for i in range(0,len(block),100):
                xi = block[i:i+100]/period
                if len(xi)<100: 
                    leftover = xi
                    break
                sums.append(sum(xi))

        end_time = time.time()
        elapsed_time = end_time - start_time
        return sums, elapsed_time
