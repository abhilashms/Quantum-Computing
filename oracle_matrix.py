"""
Quantum Oracle Matrix Generator using PennyLane

This module provides a utility to create quantum oracle matrices for Grover's algorithm.
An oracle is a diagonal unitary matrix that applies a phase flip (-1 multiplication)
to a target quantum state, marking it for amplitude amplification in search algorithms.
"""

import pennylane as qp
import numpy as np

# Create a quantum device simulator with 4 qubits
dev = qp.device("default.qubit", wires=4)

# ============================================================================
# ORACLE FUNCTION: Creates an oracle matrix for Grover's search algorithm
# ============================================================================

def oracle(combo):
    """
    Generate a quantum oracle matrix that marks a target state with a phase flip.
    
    The oracle is a diagonal unitary matrix where all diagonal elements are 1
    except for the target state index, which is -1. This phase flip is used in
    Grover's algorithm to mark the solution state during amplitude amplification.
    
    Args:
        combo (list): List of bits representing the target state to mark.
                      Example: [1, 0, 0, 1] marks the state |1001>
    
    Returns:
        np.ndarray: A 2^n x 2^n diagonal unitary matrix where n = len(combo).
                    Main diagonal contains 1s everywhere except at the combo index
                    position which contains -1.
    
    Example:
        >>> oracle([0, 0])
        array([[-1.,  0.,  0.,  0.],
               [ 0.,  1.,  0.,  0.],
               [ 0.,  0.,  1.,  0.],
               [ 0.,  0.,  0.,  1.]])
    """
    # Create an identity matrix of size 2^n (n = number of bits/qubits)
    identity_matrix = np.identity(2 ** len(combo))
    
    # Convert the binary combo list to its decimal index
    # E.g., [1, 0, 0, 1] -> index 9 (in binary: 1001 = 9 in decimal)
    index = np.ravel_multi_index(combo, [2] * len(combo))
    
    # Apply phase flip: set the target state amplitude multiplier to -1
    identity_matrix[index][index] = -1
    
    oracle_matrix = identity_matrix
    return oracle_matrix


# ============================================================================
# EXECUTION: Generate and display oracle matrix for target state
# ============================================================================

# Define the target state to mark with the oracle
# This state will have a phase flip (-1) applied to its amplitude
combo = [1, 0, 0, 1]

# Generate the oracle matrix and print it
# The matrix will show -1 at position corresponding to binary [1,0,0,1] = index 9
print(oracle(combo))