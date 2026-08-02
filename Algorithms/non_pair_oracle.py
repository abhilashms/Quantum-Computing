"""
Quantum Oracle Circuit Implementation using PennyLane

This module demonstrates a simple quantum oracle circuit without state pairing.
It implements Grover's oracle: a phase-flip operation that marks a specific target state
by applying -1 to its amplitude, which can amplify its probability when combined with
other Grover's algorithm components.
"""

import pennylane as qp
import numpy as np

# Number of qubits in the quantum circuit
n_bits = 4

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
    by -1, effectively flipping its phase relative to other states. This is a key
    component of Grover's algorithm for quantum search.
    
    Args:
        combo (list): List of bits representing the target state to mark.
                      Example: [0, 1, 0, 1] marks the state |0101>
    
    Returns:
        np.ndarray: A 2^n x 2^n unitary matrix where n = len(combo).
                    Diagonal matrix with -1 at the combo index, 1 elsewhere.
    """
    # Create an identity matrix of size 2^n (n = number of bits/qubits)
    identity_matrix = np.identity(2 ** len(combo))
    
    # Convert the binary combo list to its decimal index
    # E.g., [0, 1, 0, 1] -> index 5 (in binary: 0101 = 5 in decimal)
    index = np.ravel_multi_index(combo, [2] * len(combo))
    
    # Apply phase flip: set the target state amplitude multiplier to -1
    identity_matrix[index][index] = -1
    
    return identity_matrix


# ============================================================================
# ORACLE CIRCUIT: Quantum circuit applying Grover's oracle
# ============================================================================

@qp.qnode(dev)
def oracle_circuit(combo):
    """
    Quantum circuit that applies the oracle to mark a target state.
    
    The circuit:
    1. Prepares an equal superposition of all basis states using Hadamard gates
    2. Applies the oracle phase flip to the target state
    3. Returns the quantum state (not probabilities, to preserve phase information)
    
    Args:
        combo (list): The target state to mark with the oracle
    
    Returns:
        np.ndarray: Complex-valued quantum state vector with amplitudes.
                    Phase flips are visible in the state vector.
    
    Note:
        Using qp.probs() would return only probability magnitudes, losing
        the phase information. We use qp.state() to preserve phase flips.
    """
    # Initialize all qubits in equal superposition
    # Creates: (|0> + |1>) / sqrt(2) for each qubit, giving all 2^n states equally
    for i in range(n_bits):
        qp.Hadamard(wires=i)
    
    # Get the oracle matrix for the target combo state
    oracle_matrix = oracle(combo)
    
    # Apply the oracle unitary to all qubits
    # This flips the phase of the target state amplitude by -1
    qp.QubitUnitary(oracle_matrix, wires=range(n_bits))
    
    # Return the complete quantum state vector with phase information
    # Note: qp.probs() would return only probability magnitudes, hiding phase flips
    return qp.state()

# ============================================================================
# EXECUTION
# ============================================================================

# Define the target state to mark with the oracle (4 qubits)
combo = [0, 1, 0, 1]

# Run the quantum circuit and print the resulting state vector
# The amplitude at index 5 (binary 0101) will be negated by the oracle
print(oracle_circuit(combo))