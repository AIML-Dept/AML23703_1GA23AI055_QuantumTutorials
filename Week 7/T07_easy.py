from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import os

sim = AerSimulator()

print("Deutsch's Algorithm - Constant Function f(x) = 0\n")

qc = QuantumCircuit(2, 1)
qc.x(1)          # ancilla -> |1>
qc.h([0, 1])      # superposition on both qubits

# Oracle for f(x) = 0 (constant): does nothing to the ancilla
# (no gates added - identity oracle)

qc.h(0)           # interference on input qubit
qc.measure(0, 0)

print(qc.draw())

result = sim.run(qc, shots=1024).result()
counts = result.get_counts()
print("\nMeasurement counts:", counts)

outcome = list(counts.keys())[0]
classification = "constant" if outcome == '0' else "balanced"
print(f"\nMeasured qubit value: {outcome}")
print(f"Function classified as: {classification}")
print(f"Expected: constant  |  Match: {classification == 'constant'}")

os.makedirs("output", exist_ok=True)
with open("output/T07_easy_output.txt", "w") as f:
    f.write("Deutsch's Algorithm - Constant Function f(x) = 0\n\n")
    f.write(f"Measurement counts: {counts}\n")
    f.write(f"Measured qubit value: {outcome}\n")
    f.write(f"Function classified as: {classification}\n")
    f.write(f"Expected: constant  |  Match: {classification == 'constant'}\n")

print("\nOutput saved to output/T07_easy_output.txt")
