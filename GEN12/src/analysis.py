import numpy as np
import utils as utils
import matplotlib.pyplot as plt


# changing graphs style
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'

# --------------------------------
# reading the data obtained from src.py file to statistically 
# study the results of the tests

files = {'mt': {"name" : "data/mt_numbers.txt", "period": 2**32-1} ,
         "pcg" : {"name" : "data/pcg_numbers.txt", "period" : 2**32-1},
         "lcg" : {"name" : "data/lcg_numbers.txt" , "period": 2**31-1}}

names = files.keys()

# choosing a dictionary to save the files
results = {name: {"hist": [], "diff": [], "sums": []} for name in names}


with open('out.txt', 'r') as input_file:

    # reading header
    header = input_file.readline().strip().split()

    # printing the result in order to check that everything is correct
    print(header)

    for line in input_file:

        values = list(map(float, line.strip().split()))
        
        for idx, name in enumerate(names):
            # each algorithm has 3 columns: (hist, diff, sums)
            hist_value = values[3 * idx]
            diff_value = values[3 * idx + 1]
            sums_value = values[3 * idx + 2]

            # saving only the values which are not 0
            if hist_value != 0:
                results[name]["hist"].append(hist_value)
            if diff_value != 0:
                results[name]["diff"].append(diff_value)
            if sums_value != 0:
                results[name]["sums"].append(sums_value)



#--------permutation test--------------


# for generator_name, generator_results in results.items():

#     print(f"\nAnalyzing generator: {generator_name}")

#     data = generator_results["hist"]
    

#     group_size = 5 # grouping elements for more clarity in the graphs

#     grouped_data = np.add.reduceat(data, np.arange(0, len(data), group_size))

#     stats = utils.Statistics(grouped_data)

#     a_fit, std_a = stats.analysis_uniform_distribution()

#     x = np.arange(0,120, group_size)
#     x2 = x + group_size/2

#     plt.figure(figsize=(10, 6))
#     plt.bar(x2, grouped_data, width = group_size - 0.1, alpha=0.65, color = 'blue', edgecolor = 'black', label = 'Experimental values')
#     plt.errorbar(x2, grouped_data, yerr = np.sqrt(grouped_data), fmt='bo', ecolor = 'blue', capsize=3)
#     plt.plot(x2, utils.constant(x2, a_fit), 'o', color = 'black', label = 'Theoretical values' )
#     plt.xlabel('Permutation')
#     plt.ylabel('\# counts')
#     plt.legend()
#     plt.savefig(f'results/permutation_{generator_name}.png')
#     plt.show()


# ---------birthday spacing-----

# for generator_name, generator_results in results.items():

#     print(f"\nAnalyzing generator: {generator_name}")

#     print("Data stats:", np.min(generator_results["diff"]), np.max(generator_results["diff"]), np.mean(generator_results["diff"]))

#     data = generator_results["diff"]
    
#     n_bins = 20
#     filtered_counts, filtered_edges, filtered_centers, bin_width, mu, yerr = utils.Statistics(data).analysis_diff(n_bins)

#     plt.figure(figsize=(10, 6))
#     plt.bar(filtered_centers, filtered_counts, width = bin_width - 0.1, alpha=0.65, color = 'blue', edgecolor = 'black', label = 'Experimental values')
#     plt.errorbar(filtered_centers, filtered_counts, yerr = yerr, fmt='bo', ecolor = 'blue', capsize=3)
#     plt.plot(filtered_centers, utils.exponential(filtered_centers, mu), 'o', color = 'black', label = 'Theoretical values' )
#     #plt.yscale('log')  # Escala logarítmica para visualizar mejor
#     plt.legend()
#     plt.title('Histogram and Exponential Fit')
#     plt.savefig(f'results/exp_{generator_name}.png')
#     plt.show()


# # ------ overlapping sum -----------

for generator_name, generator_results in results.items():

    print(f"\nAnalyzing generator: {generator_name}")

    print("Data stats:", np.min(generator_results["sums"]), np.max(generator_results["sums"]), np.mean(generator_results["sums"]))

    data = generator_results["sums"]
    
    n_bins = 25

    filtered_counts, filtered_centers, bin_width, mu, sigma, yerr = utils.Statistics(data).analysis_sums(n_bins)

    plt.figure(figsize=(10, 6))
    plt.bar(filtered_centers, filtered_counts, width = bin_width, alpha=0.65, color = 'blue', edgecolor = 'black', label = 'Experimental values')
    plt.errorbar(filtered_centers, filtered_counts, yerr = yerr, fmt='bo', ecolor = 'blue', capsize=3)
    plt.plot(filtered_centers, utils.gaussian(filtered_centers, mu, sigma), 'o', color = 'black', label = 'Theoretical values' )
    plt.legend()
    plt.title('Histogram and Gaussian Fit')
    plt.savefig(f'results/gauss_{generator_name}.png')
    plt.show()