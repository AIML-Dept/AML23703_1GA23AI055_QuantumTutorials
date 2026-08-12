import random
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

random.seed(42)  # remove this line for a fresh random sequence each run

available_gates = ['x', 'y', 'z', 'h', 's', 't']
gate_sequence = [random.choice(available_gates) for _ in range(5)]
print(f"Randomly chosen gate sequence (applied left to right): {gate_sequence}")

# --- Simulation using Qiskit ---
qc = QuantumCircuit(1)
for gate in gate_sequence:
    getattr(qc, gate)(0)

sv_sim = Statevector.from_instruction(qc)
print("\nCircuit diagram:")
print(qc.draw(output='text'))
print(f"\nStatevector from Qiskit simulation: {sv_sim}")

# --- Analytical verification: multiply gate matrices by hand ---
gate_matrices = {
    'x': np.array([[0, 1], [1, 0]]),
    'y': np.array([[0, -1j], [1j, 0]]),
    'z': np.array([[1, 0], [0, -1]]),
    'h': (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]]),
    's': np.array([[1, 0], [0, 1j]]),
    't': np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]]),
}

state = np.array([1, 0], dtype=complex)  # start in |0>
for gate in gate_sequence:
    state = gate_matrices[gate] @ state  # matrix-vector product

print(f"\nStatevector from manual matrix multiplication: {np.round(state, 4)}")

match = sv_sim.equiv(Statevector(state))
print(f"\nDo simulation and analytical result match (up to global phase)? {match}")
print(f"\nFinal measurement probabilities: {sv_sim.probabilities_dict()}")