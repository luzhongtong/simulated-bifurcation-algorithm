import numpy as np
from time import time
from statistics import stdev

class SymplecticEulerScheme():

    def __init__(
        self, 
        matrix : np.ndarray, 
        vector : np.ndarray,
        kerr_constant : float = 1,
        detuning_frequency : float = 1,
        pressure = lambda t : 0.01 * t,
        time_step : float = 0.01,
        simulation_time : int = 600,
        symplectic_parameter : int = 2
    ) -> None:

        # Data
        
        self.matrix = matrix
        self.vector = vector 
        self.dimension = np.shape(matrix)[0]
 
        # Hamiltonian parameters
 
        self.kerr_constant = kerr_constant
        self.detuning_frequency = detuning_frequency

        # Hamiltonian functions

        self.pressure = pressure
        self.A = lambda t : 0 if (self.pressure(t) < self.detuning_frequency) else ((self.pressure(t) - self.detuning_frequency) / self.kerr_constant)**(1/2)
        
        # Simulation parameters
        
        self.time_step = time_step
        self.simulation_time = simulation_time
        self.number_of_steps = int(simulation_time / time_step)

        # Symplectic parameter

        self.symplectic_parameter = symplectic_parameter
        self.symplectic_time_step = time_step / symplectic_parameter

        # Parameters calculated from matrix
        
        self.xi0 = 0.7 * detuning_frequency / (stdev([self.matrix[i][matrix] for i in range(self.dimension) for matrix in range(self.dimension) if i != matrix]) * (self.dimension)**(1/2))
        self.diag_matrix_column = np.array([np.diag(self.matrix)]).T

        # Constant

        self.unit_column = np.ones((self.dimension, 1))

    def run(
        self, 
        display_time = True
    ):

        # Initialization of the oscillators

        X = np.zeros((self.dimension,1)) 
        Y = np.zeros((self.dimension,1)) 

        # Begining of simulation

        start_time = time()

        for step in range(self.number_of_steps):

            current_time = step * self.time_step
            current_pressure = self.pressure(current_time)

            # Symplectic loops

            for _ in range(self.symplectic_parameter):

                X += self.symplectic_time_step * (((self.detuning_frequency + current_pressure) * self.unit_column - self.xi0 * self.diag_matrix_column) * Y)
                Y -= self.symplectic_time_step * (X**3 + (self.detuning_frequency - current_pressure) * X)  

            Y += self.xi0 * (self.matrix @ X - 2 * self.A(current_time) * self.vector) * self.time_step

        end_time = time()

        # End of simulation

        simulation_time = round((end_time - start_time) * 100) / 100

        if display_time:    

            print(f"Run in {simulation_time} seconds.")

        # Returning the result    

        return np.sign(X)   