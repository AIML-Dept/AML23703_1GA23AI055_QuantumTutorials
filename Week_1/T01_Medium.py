"""
Tutorial No. : T01 | Date: 23-07-2026 | Level: Medium
Objective    : 1-qubit Hadamard circuit, measure, 1024 shots, plot histogram.
USN          : 1GA23AI055
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

counts = AerSimulator().run(transpile(qc, AerSimulator()), shots=1024).result().get_counts()

print(counts)
plot_histogram(counts, title="1-Qubit Hadamard Superposition")
plt.savefig("Output_T01_Medium.png")
plt.show()