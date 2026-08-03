import pennylane as qp

dev = qp.device("default.qubit")

@qp.qnode(dev)
def BasisEmbedding(value):
    qp.BasisEmbedding(features = value , wires = range(3))
    return qp.state()
# print(BasisEmbedding([0,1,1]))
print(BasisEmbedding(6))