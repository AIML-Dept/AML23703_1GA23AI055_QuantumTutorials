from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import os

sim = AerSimulator()

print("Deutsch's Algorithm - Balanced Function f(x) = x\n")

qc = QuantumCircuit(2, 1)
qc.x(1)
qc.h([0, 1])

# Oracle for f(x) = x (balanced): CNOT(input, ancilla)
qc.cx(0, 1)

qc.h(0)
qc.measure(0, 0)

print(qc.draw())

result = sim.run(qc, shots=1024).result()
counts = result.get_counts()
print("\nMeasurement counts:", counts)

outcome = list(counts.keys())[0]
classification = "constant" if outcome == '0' else "balanced"
print(f"\nMeasured qubit value: {outcome}")
print(f"Function classified as: {classification}")
print(f"Expected: balanced  |  Match: {classification == 'balanced'}")

os.makedirs("output", exist_ok=True)
with open("output/T07_medium_output.txt", "w") as f:
    f.write("Deutsch's Algorithm - Balanced Function f(x) = x\n\n")
    f.write(f"Measurement counts: {counts}\n")
    f.write(f"Measured qubit value: {outcome}\n")
    f.write(f"Function classified as: {classification}\n")
    f.write(f"Expected: balanced  |  Match: {classification == 'balanced'}\n")

print("\nOutput saved to output/T07_medium_output.txt")
