from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

qc = QuantumCircuit(1)
qc.h(0)
qc.z(0)

sv = Statevector.from_instruction(qc)

# Theoretical |-> state = (|0> - |1>)/sqrt(2)
minus_state = Statevector([1/np.sqrt(2), -1/np.sqrt(2)])

print("Circuit (H followed by Z):")
print(qc.draw(output='text'))
print(f"\nSimulated statevector: {sv}")
print(f"Expected |-> state:    {minus_state}")

match = sv.equiv(minus_state)  # allows for global phase differences
print(f"\nDoes simulation match theoretical |-> state (up to global phase)? {match}")
print(f"\nMeasurement probabilities: {sv.probabilities_dict()}")