from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

qc = QuantumCircuit(1)
qc.x(0)

sv = Statevector.from_instruction(qc)

print(qc.draw())
print(sv)

for i, amp in enumerate(sv):
    print(f"|{i}>: {amp}")

sv.draw("bloch")