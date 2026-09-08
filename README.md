# Hybrid Maximum Power Point Tracking Techniques: Review and Comparison under Partial Shading Conditions
This repository contains the most relevant hybrid Global Maximum Power Point Tracking (GMPPT) methods reported in the literature and compares their performance under a
common experimental framework. This work was developed by Nicolas Yañez-Monsalvez, Catalina González-Castaño, Carlos Restrepo, Cristian Guarnizo-Lemus, Sebastián
Riffo, and Samir Kouro. Real world experiments were carried out at Laboratorio de Aplicaciones en Redes Inteligentes ([LARI](https://www.instagram.com/lari.utalca/)), Universidad de Talca, Chile. 

## Experiments in Python
Before implementing the MPPT methods in the PLECS platform, each method is tested in Python. 
* Characterization of a commercial Panasonic EverVolt 380W panel:  The code [PV_module_characterized.py](https://github.com/cdguarnizo/Hybrid_MPPT_Comparison/blob/main/PV_module_characterized.py) includes the simulations and data generation for this panel at different shading conditions. These simulations are performed using the library [PVMismatch](https://github.com/SunPower/PVMismatch/) from SunPower.

### Standard approach
* Perturb and Observe (P&O):


### Supervised Learning models
* Decision Trees:
* Neural networks (multilayer perceptron):

### Metaheuristic Optimization
* Genetic Algorihtnms:
* Particle Swarm Optimization:

## Implementations in PLECS platform


