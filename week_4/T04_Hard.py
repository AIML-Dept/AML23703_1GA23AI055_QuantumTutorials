from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

qc = QuantumCircuit(3, 3)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 2)      # Extend entanglement to third qubit
qc.measure([0, 1, 2], [0, 1, 2])

print(qc.draw())

sim = AerSimulator()
result = sim.run(qc, shots=1024).result()
counts = result.get_counts()
print("Counts:", counts)   # Expect only '000' and '111'
plot_histogram(counts)