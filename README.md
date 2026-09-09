# Hybrid Maximum Power Point Tracking Techniques: Review and Comparison under Partial Shading Conditions
This repository contains the most relevant hybrid Global Maximum Power Point Tracking (GMPPT) methods reported in the literature and compares their performance under a
common experimental framework. This work was developed at Laboratorio de Aplicaciones en Redes Inteligentes ([LARI](https://www.instagram.com/lari.utalca/)), Universidad de Talca, Chile. 

## Experiments in Python
Before implementing the MPPT methods in the PLECS platform, each method is tested in Python. 
* Characterization of a commercial Panasonic EverVolt 380W panel:  The code [PV_module_characterized.py](https://github.com/cdguarnizo/Hybrid_MPPT_Comparison/blob/main/PV_module_characterized.py) includes the simulations and data generation for this panel at different shading conditions. These simulations are performed using the library [PVMismatch](https://github.com/SunPower/PVMismatch/) from SunPower. The dataset is saved with the following columns: Columns 0 - 2: Shading pattern; Column 3: Index of the maximum power point (0,1,2). Column 4: Maximum voltage. Column 5: Maximum power. Columns 6-8: Voltage local maxima. Columns 9-11: Power local maxima.

### Standard approach
* Perturb and Observe (P&O): There are two simulations to test the performance of P&O, in *GMPPT_Perturb_&_Observe_Delta.py*, the P&O algorithm is teste for one shading condition. Meanwhile, in *GMPPT_Perturb_&_Observe_Time.py*, the algorithm is tested against three different shading conditions.

### Supervised Learning models
The following approaches are trained using the dataset obtained from the simulations of *PV_module_characterized.py* and registered in *dataset.csv*.
* Decision Trees: We trained three different decision trees for each of the main voltages (10V, 20V and 40V) formed by the shading conditions. The inputs of the decision threes are the local maxima voltages and powers of each P-V curve. 
* Neural networks (multilayer perceptron): Similar to the Decision trees case, Artificial Neural Newtorks are trained for each of the main voltages (10V, 20V and 40V).

### Metaheuristic Optimization
* Genetic Algorithms: In the python file *Genetic_Algorithm_and_Perturb_&_Observe.py* is coded a Genetic Algorithm combined with P&O aimed to find de MPPT.
* Particle Swarm Optimization: In the python file *Particle_Swarm_Optimization_and_Perturb_&_Observe.py* is coded a Particle Swarm Algorithm combined with P&O aimed to find the MPPT.

## Implementations in PLECS platform
In the folder PLECS is the code source of the Hybrid approaches coded to find the MPPT.

