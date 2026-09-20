from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import os

sim = AerSimulator()

def build_oracle(qc, q_in, q_anc, function_type):
    """Dynamically builds the oracle for one of the four possible single-bit functions."""
    if function_type == "constant_0":
        pass  # f(x) = 0 : identity, no gates
    elif function_type == "constant_1":
        qc.x(q_anc)  # f(x) = 1 : flip ancilla unconditionally
    elif function_type == "balanced_identity":
        qc.cx(q_in, q_anc)  # f(x) = x
    elif function_type == "balanced_not":
        qc.cx(q_in, q_anc)  # f(x) = NOT x
        qc.x(q_anc)
    else:
        raise ValueError(f"Unknown function type: {function_type}")

def run_deutsch(function_type):
    qc = QuantumCircuit(2, 1)
    qc.x(1)
    qc.h([0, 1])
    build_oracle(qc, 0, 1, function_type)
    qc.h(0)
    qc.measure(0, 0)
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()
    outcome = list(counts.keys())[0]
    classification = "constant" if outcome == '0' else "balanced"
    return counts, outcome, classification

function_types = {
    "constant_0": "constant",
    "constant_1": "constant",
    "balanced_identity": "balanced",
    "balanced_not": "balanced",
}

print("Deutsch's Algorithm - Generic Oracle-Selection Test\n")
print(f"{'Function type':^20}{'Expected':^12}{'Measured':^12}{'Classified':^14}{'Match':^8}")
print("-" * 66)

all_results = []
for ftype, expected in function_types.items():
    counts, outcome, classification = run_deutsch(ftype)
    match = classification == expected
    all_results.append((ftype, expected, outcome, classification, match))
    print(f"{ftype:^20}{expected:^12}{outcome:^12}{classification:^14}{str(match):^8}")

all_ok = all(r[4] for r in all_results)
print(f"\nAll four oracle types classified correctly: {all_ok}")

os.makedirs("output", exist_ok=True)
with open("output/T07_hard_output.txt", "w") as f:
    f.write("Deutsch's Algorithm - Generic Oracle-Selection Test\n\n")
    f.write(f"{'Function type':^20}{'Expected':^12}{'Measured':^12}{'Classified':^14}{'Match':^8}\n")
    f.write("-" * 66 + "\n")
    for ftype, expected, outcome, classification, match in all_results:
        f.write(f"{ftype:^20}{expected:^12}{outcome:^12}{classification:^14}{str(match):^8}\n")
    f.write(f"\nAll four oracle types classified correctly: {all_ok}\n")

print("\nOutput saved to output/T07_hard_output.txt")
