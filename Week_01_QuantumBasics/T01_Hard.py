"""
Tutorial No.   : T01
Date           : 23-07-2026
Objective      : 3-qubit equal superposition, verify uniform 1/8 distribution.
Student Name   : <YOUR NAME>
USN            : 1GA23AI055
Level          : Hard
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

qc = QuantumCircuit(3, 3)
qc.h([0, 1, 2])
qc.measure([0, 1, 2], [0, 1, 2])

result = AerSimulator().run(transpile(qc, AerSimulator()), shots=8192).result()
counts = result.get_counts()

print(counts)
for state, count in sorted(counts.items()):
    print(state, count / 8192, "(theory: 0.125)")

plot_histogram(counts, title="3-Qubit Equal Superposition")
plt.savefig("Output_T01_Hard.png")
plt.show()