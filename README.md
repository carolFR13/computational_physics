# Advanced Computational Physics: Simulation Methods

Solutions for the following exercises: 

[GEN12] Study algorithms of the PCG family: permuted congruential generators.Implement a basic algorithm and check the statistical properties.

[MUE5] Generate random numbers (θ,φ) in spherical coordinates such that the distribution of directions is homogeneous (isotropic) over the surface of a sphere centred at the origin. Show the distributions of the variables θ and φ.

[INC2] Determine the integral of f(x)= e^(-x) on the interval [0,1] using the two methods defined for the calculation of integrals. Perform the calculation for n=100, 1000 and 10000. Calculate the standard deviation in each case. Compare the result with what is expected from the formulae for the dependence of the error on n.

[INT3] Compute the given integral in 5 dimensions.

[PRO1] Monty Hall Problem: In a quiz show, the player is presented with three closed boxes, one of which contains a prize. The player chooses one of the boxes and the presenter, who knows which box contains the prize, removes one of the unchosen boxes (which obviously does not contain the prize) and asks the player to decide whether to keep his previous choice or switch boxes. Write a programme that analyses the player's chances of winning the prize based on their decision to keep their choice or switch boxes.

[ALE5] Perform a simulation to determine a potential map in a 10x20x30cm3 box whose top and bottom sides have a voltage of 100V and whose walls are earthed, using the random walk Laplace function evaluation method. Plot a 2D histogram of the potential in the horizontal and vertical symmetrical shear planes of the box.


[COL2] Classical ideal gas in one dimension. Microcanonical Monte Carlo simulation. We will implement the code that allows the simulation of an ideal gas in one dimension. We will use the following features:
- The energy does not depend on the position of the particles.
- The total energy is the sum of the kinetic energies of the individual particles.
- Each time we change the configuration, we will randomly change the velocity of one of the particles and recalculate the energy.
