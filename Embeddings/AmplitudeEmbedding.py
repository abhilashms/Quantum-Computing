import pennylane as qp

dev = qp.device("default.qubit")

@qp.qnode(dev)
def AmplitudeEmbedding(amplitudes):
    qp.AmplitudeEmbedding(features = amplitudes, wires = range(1), normalize = True , pad_with =0)
    return qp.state()

print(AmplitudeEmbedding([0.5,0.5]))
