from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

qc = QuantumCircuit(1)
qc.h(0)

sv_ideal = Statevector.from_instruction(qc)

random_phase = np.random.uniform(0, 2 * np.pi)
qc.p(random_phase, 0)

sv_noisy = Statevector.from_instruction(qc)

print(qc.draw())
print(f"Random phase error introduced: {random_phase} radians")

print("\nIdeal Statevector:")
print(sv_ideal)

print("\nNoisy Statevector:")
print(sv_noisy)

sv_ideal.draw("bloch")
sv_noisy.draw("bloch")