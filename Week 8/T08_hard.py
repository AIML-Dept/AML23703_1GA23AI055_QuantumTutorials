from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import os

sim = AerSimulator()

def build_dj_circuit(n, function_type):
    qc = QuantumCircuit(n + 1, n)
    qc.x(n)
    qc.h(range(n + 1))

    if function_type == "constant":
        pass  # f(x) = 0, identity oracle
    elif function_type == "balanced":
        for i in range(n):
            qc.cx(i, n)  # parity oracle
    else:
        raise ValueError(f"Unknown function type: {function_type}")

    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc

def run_dj(n, function_type):
    qc = build_dj_circuit(n, function_type)
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()
    outcome = list(counts.keys())[0]
    classification = "constant" if outcome == '0' * n else "balanced"
    return outcome, classification

print("Deutsch-Jozsa Algorithm - Generalised for n = 2 to 5\n")
print(f"{'n':^4}{'Function type':^16}{'Measured':^12}{'Classified':^14}{'Match':^8}")
print("-" * 54)

all_results = []
for n in range(2, 6):
    for function_type in ["constant", "balanced"]:
        outcome, classification = run_dj(n, function_type)
        match = classification == function_type
        all_results.append((n, function_type, outcome, classification, match))
        print(f"{n:^4}{function_type:^16}{outcome:^12}{classification:^14}{str(match):^8}")

all_ok = all(r[4] for r in all_results)
print(f"\nAll cases (n=2 to 5, both function types) classified correctly: {all_ok}")

os.makedirs("output", exist_ok=True)
with open("output/T08_hard_output.txt", "w") as f:
    f.write("Deutsch-Jozsa Algorithm - Generalised for n = 2 to 5\n\n")
    f.write(f"{'n':^4}{'Function type':^16}{'Measured':^12}{'Classified':^14}{'Match':^8}\n")
    f.write("-" * 54 + "\n")
    for n, function_type, outcome, classification, match in all_results:
        f.write(f"{n:^4}{function_type:^16}{outcome:^12}{classification:^14}{str(match):^8}\n")
    f.write(f"\nAll cases classified correctly: {all_ok}\n")

print("\nOutput saved to output/T08_hard_output.txt")
