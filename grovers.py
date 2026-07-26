import numpy as np
import pennylane as qp

n_bits = 4
aux = [n_bits]
query = list(range(n_bits))
all_wire = query+aux
combo = [0, 0,0,0] 

dev = qp.device("default.qubit", wires =len(all_wire))

# @qp.qnode(dev)
def oracle():
    qp.MultiControlledX(
        wires=all_wire,
        control_values=combo   # matches |0110⟩
    )
    # return qp.state()
# @qp.qnode(dev)
def difusion():
    for i in range(len(query)):
        qp.Hadamard(wires=i)
    
    qp.MultiControlledX(
        wires=all_wire,
        control_values=[0, 0, 0, 0]
    )
    for i in range(len(query)):
        qp.Hadamard(wires=i)
    # return qp.state()

@qp.qnode(dev)
def main():
    qp.PauliX(wires = aux)
    for i in range(len(all_wire)):
        qp.Hadamard(wires=i)
    for _ in range(int(np.sqrt(n_bits))):
        oracle()
        
        difusion()
    return qp.probs(wires = query)


print(main())
