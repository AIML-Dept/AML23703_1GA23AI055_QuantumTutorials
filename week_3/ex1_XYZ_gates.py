from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

gates = ['x', 'y', 'z']

for gate in gates:
    qc = QuantumCircuit(1)
    getattr(qc, gate)(0)          # apply the gate: qc.x(0), qc.y(0), qc.z(0)
    sv = Statevector.from_instruction(qc)

    print(f"Circuit after applying {gate.upper()} gate:")
    print(qc.draw(output='text'))
    print(f"Resulting statevector: {sv}")
    print(f"Probabilities: {sv.probabilities_dict()}")
    print("-" * 50)