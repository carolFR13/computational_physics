import numpy as np
import matplotlib.pyplot as plt
import utils as utils


# Changing graphs style
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'


#_______________________________________________________
# Let's start by analyzing the time each generator
# spent generating 10**8 numbers


file_name = 'data/algorithm_times.txt'

data = utils.Read(file_name).read_file(header = True) # reading time file as a whole

# computing means and std 
means = [utils.Statistics.mean(x/1000) for x in data]

stds = [utils.Statistics.std(x/1000) for x in data] 

# plotting results

x = range(len(data))

plt.errorbar(x,means, yerr = stds, capsize = 3, fmt='ro', ecolor = 'black')
plt.ylabel(r't(s)')
plt.xticks(x, labels= ["MT", "PCG", "LCG"])
plt.grid(alpha=0.3)
plt.xlim(-0.5,2.5)
plt.savefig('results/time_comparation.png')
plt.show()


#___________________________________________________
# We will now perform some of the Diehard tests for 
# the different algorithms 

files = {'mt': {"name" : "data/mt_numbers.txt", "period": 2**32-1} ,
         "pcg" : {"name" : "data/pcg_numbers.txt", "period" : 2**32-1},
         "lcg" : {"name" : "data/lcg_numbers.txt" , "period": 2**31-1}}

names = files.keys()
print(names)

hist = {} ; diff = {} ; sums = {}
for name in names:

    name_path = files[name]["name"]
    period = files[name]["period"]


    #--------permutation test--------------

    hist[name], elapsed_time = utils.Diehard_tests(name_path).overlapping_permutations()
    print(f"Execution time for overlapping permutation test: {elapsed_time:.6f} s for ", name, " method")


    # ---------birthday spacing-----

    diff[name], elapsed_time = utils.Diehard_tests(name_path).birthday_spacing()
    print(f"Execution time for birthday spacing test: {elapsed_time:.6f} s for ", name, " method")


    #------ overlapping sum -----------

    sums[name], elapsed_time = utils.Diehard_tests(name_path).overlapping_sum(period)
    print(f"Execution time for overlapping sum test: {elapsed_time:.6f} s for ", name, " method")




# output file with the results of each test for each algorithm in order to analyse the data
with open('out.txt', 'w') as output:
    # names for the header
    header = []
    for algorithm in names:
        header.extend([f"Hist_{algorithm}", f"All_Diff_{algorithm}", f"Sums_{algorithm}"])
    output.write(" ".join(header) + "\n")

    # find the maximum length among all the lists
    max_len = max(
        max(len(hist[name]) for name in names),
        max(len(diff[name]) for name in names),
        max(len(sums[name]) for name in names)
    )
    
    # writing lines with the results
    for i in range(max_len):
        row = []
        
        # result for each algorithm, completing with 0 if needed
        for name in names:
            hist_value = hist[name][i] if i < len(hist[name]) else 0
            diff_value = diff[name][i] if i < len(diff[name]) else 0
            sums_value = sums[name][i] if i < len(sums[name]) else 0
            
            # adding the values in each line
            row.extend([str(hist_value), str(diff_value), str(sums_value)])
        
        # writing the row
        output.write(" ".join(row) + "\n")
