import random
import matplotlib.pyplot as plt
from scipy.stats import chisquare
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

NUM_BITS = 4         
COUNT = 1000

qc = QuantumCircuit(NUM_BITS, NUM_BITS)
qc.h(range(NUM_BITS))
qc.measure(range(NUM_BITS), range(NUM_BITS))

sim = AerSimulator()
result = sim.run(transpile(qc, sim), shots=COUNT, memory=True).result()
quantum_numbers = [int(b, 2) for b in result.get_memory()]

classical_numbers = [random.randint(0, 2**NUM_BITS - 1) for _ in range(COUNT)]

q_freq = [quantum_numbers.count(v) for v in range(2**NUM_BITS)]
c_freq = [classical_numbers.count(v) for v in range(2**NUM_BITS)]

print("Quantum RNG chi-square:", chisquare(q_freq))
print("Classical RNG chi-square:", chisquare(c_freq))

fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].bar(range(16), q_freq); ax[0].set_title("Quantum RNG")
ax[1].bar(range(16), c_freq); ax[1].set_title("Classical RNG")
plt.savefig("Output_T01_Realworld.png")
plt.show()
