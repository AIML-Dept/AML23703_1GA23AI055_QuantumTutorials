import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# H gate creates equal superposition -> fair "quantum coin"
# |0> = Heads, |1> = Tails; player wins on Heads

qc = QuantumCircuit(1)
qc.h(0)

sv = Statevector.from_instruction(qc)
probs = sv.probabilities_dict()

print("Quantum coin-flip circuit:")
print(qc.draw(output='text'))
print(f"\nTheoretical probabilities: {probs}")

np.random.seed(1)  # remove for different random results each run
num_games = 10000
outcomes = sv.sample_counts(num_games)  # built-in Qiskit sampling, no Aer needed

heads = outcomes.get('0', 0)
tails = outcomes.get('1', 0)
win_probability = heads / num_games

print(f"\nPlayed {num_games} games.")
print(f"Heads (win): {heads}  |  Tails (lose): {tails}")
print(f"Empirical win probability: {win_probability:.4f}")
print(f"Theoretical win probability: {probs.get('0', 0):.4f}")