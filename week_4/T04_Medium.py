from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

qc = QuantumCircuit(2, 2)
qc.h(0)          # Superposition on q0
qc.cx(0, 1)      # Entangle q0 and q1
qc.measure([0, 1], [0, 1])

print(qc.draw())

sim = AerSimulator()
result = sim.run(qc, shots=1024).result()
counts = result.get_counts()
print("Counts:", counts)   # Expect only '00' and '11'
plot_histogram(counts)