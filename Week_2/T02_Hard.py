from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

qc = QuantumCircuit(2)
qc.h(0)
qc.h(1)

sv = Statevector.from_instruction(qc)

print(qc.draw())
print(sv)

total = 0
for i, amp in enumerate(sv):
    prob = np.abs(amp) ** 2
    total += prob
    print(f"|{i:02b}>: amplitude = {amp}, probability = {prob}")

print(f"\nSum of squared amplitudes = {total}")

sv.draw("bloch")