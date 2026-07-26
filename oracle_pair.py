"""
Quantum Oracle Pairing Implementation using PennyLane

This module implements a quantum oracle for searching through paired quantum states.
It uses Grover's algorithm-like approach with an oracle that marks a specific state
by applying a phase shift (multiplication by -1) to the target state amplitude.
"""

import pennylane as qp
import numpy as np
from itertools import product

# Number of qubits/bits for the quantum circuit
n_bits = 5

# Target combination to mark with the oracle phase flip
combo = [0, 0, 1, 1, 0]

# Create a quantum device simulator with 'n_bits' qubits
dev = qp.device("default.qubit", wires=n_bits)

# ============================================================================
# ORACLE FUNCTION: Creates an oracle matrix for Grover's search algorithm
# ============================================================================

def oracle(combo):
    """
    Create a quantum oracle matrix that marks the target state with a phase flip.
    
    The oracle is implemented as a diagonal matrix (identity with -1 at target state).
    When applied to a quantum state, it multiplies the amplitude of the target state
    by -1, effectively flipping its phase relative to other states.
    
    Args:
        combo (list): List of bits representing the target state to mark.
                      Example: [0, 0, 0, 1, 0] marks the 3rd (4th in 0-indexed) state
    
    Returns:
        np.ndarray: A 2^n x 2^n unitary matrix where n = len(combo).
                    Diagonal matrix with -1 at the combo index, 1 elsewhere.
    """
    # Create an identity matrix of size 2^n (n = number of bits/qubits)
    identity_matrix = np.identity(2 ** len(combo))
    
    # Convert the binary combo list to its decimal index
    # E.g., [0, 0, 0, 1, 0] -> index 2 (counting from 0)
    index = np.ravel_multi_index(combo, [2] * len(combo))
    
    # Apply phase flip: set the target state amplitude multiplier to -1
    identity_matrix[index][index] = -1
    
    oracle_matrix = identity_matrix
    return oracle_matrix


# ============================================================================
# PAIRING ORACLE QUANTUM CIRCUIT
# ============================================================================

@qp.qnode(dev)
def pairing_oracle(x_tilde,combo):
    """
    Quantum circuit implementing Grover's search with an oracle for paired states.
    
    The circuit:
    1. Initializes the first (n-1) qubits to basis states based on x_tilde pairs
    2. Places the last qubit in superposition using Hadamard
    3. Applies the oracle phase flip to the target state
    4. Applies Hadamard to amplify the marked state
    5. Measures the probability distribution
    
    Args:
        combo (list): The target state to search for
    
    Returns:
        np.ndarray: Probability distribution over all 2^n basis states
    """
    
    # Generate all (n-1)-bit strings for pairing
    # E.g., for n_bits=5, generates all 4-bit binary strings: 0000, 0001, ..., 1111
    
    # Initialize the first (n-1) qubits according to x_tildes[i]
    # Apply Pauli-X gates where the bit is 1 to set up basis states
    for i in range(n_bits-1):
        if x_tilde[i] == 1:
            qp.PauliX(wires=i)
    
    # Place the last qubit in equal superposition using Hadamard gate
    # This creates: (|0> + |1>) / sqrt(2) on the last qubit
    qp.Hadamard(wires=n_bits-1)
    
    # Get the oracle matrix for the target combo state
    oracle_matrix = oracle(combo)
    
    # Apply the oracle unitary to all qubits
    # This flips the phase of the target state amplitude
    qp.QubitUnitary(oracle_matrix, wires=range(n_bits))
    
    # Apply Hadamard again to amplify the marked state probability
    # This is the amplitude amplification step in Grover's algorithm
    qp.Hadamard(wires=n_bits-1)
    
    # Return probability distribution over all basis states
    return qp.probs(wires = n_bits-1)


# ============================================================================
# EXECUTION
# ============================================================================

# Run the quantum circuit with the target combo and print probability results

def pair_lock_picker():
    x_tilde_strs = [np.binary_repr(n, n_bits-1) for n in range(2**(n_bits-1))]
    
    # Convert binary strings to lists of integers
    # E.g., "0101" -> [0, 1, 0, 1]
    x_tildes = [[int(s) for s in x_tilde_str] for x_tilde_str in x_tilde_strs]
  
    for x_tilde in x_tildes:
        probability_1= pairing_oracle(x_tilde,combo)[1]
        if np.isclose(probability_1,1):
            chance_1 = x_tilde+[1]
            chance_2 = x_tilde+[0]
            if combo == chance_1:
                print(f"our right answer is = {chance_1}")
            else:
                print(f"our right answer is = {chance_2}")
            return None
    print(f"no solution found for {combo}")
    return None
    
pair_lock_picker()

