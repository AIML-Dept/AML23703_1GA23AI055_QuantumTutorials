from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import os

n = 3
sim = AerSimulator()

print(f"Deutsch-Jozsa Algorithm - Balanced Parity Function, n = {n}\n")

qc = QuantumCircuit(n + 1, n)
qc.x(n)
qc.h(range(n + 1))

# Oracle for balanced parity function f(x) = x0 XOR x1 XOR ... XOR x(n-1)
for i in range(n):
    qc.cx(i, n)

qc.h(range(n))
qc.measure(range(n), range(n))

print(qc.draw())

result = sim.run(qc, shots=1024).result()
counts = result.get_counts()
print("\nMeasurement counts:", counts)

outcome = list(counts.keys())[0]
classification = "constant" if outcome == '0' * n else "balanced"
print(f"\nMeasured bitstring: {outcome}")
print(f"Function classified as: {classification}")
print(f"Expected: balanced  |  Match: {classification == 'balanced'}")

os.makedirs("output", exist_ok=True)
with open("output/T08_medium_output.txt", "w") as f:
    f.write(f"Deutsch-Jozsa Algorithm - Balanced Parity Function, n = {n}\n\n")
    f.write(f"Measurement counts: {counts}\n")
    f.write(f"Measured bitstring: {outcome}\n")
    f.write(f"Function classified as: {classification}\n")
    f.write(f"Expected: balanced  |  Match: {classification == 'balanced'}\n")

print("\nOutput saved to output/T08_medium_output.txt")
