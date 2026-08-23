"""
Tutorial 5 - EASY Exercise
Measure a Hadamard-superposition qubit with 100, 1000 and 10000 shots
and tabulate how the measured probability converges to 0.5.
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def build_circuit():
    qc = QuantumCircuit(1, 1)
    qc.h(0)            # create equal superposition
    qc.measure(0, 0)
    return qc


def run_shots(qc, shots, backend):
    tqc = transpile(qc, backend)
    result = backend.run(tqc, shots=shots).result()
    counts = result.get_counts()
    p1 = counts.get('1', 0) / shots
    return counts, p1


if __name__ == "__main__":
    backend = AerSimulator()
    qc = build_circuit()

    shot_list = [100, 1000, 10000]

    print(f"{'Shots':>8} | {'Counts':>28} | {'P(|1>)':>8} | {'|P - 0.5|':>10}")
    print("-" * 65)
    for shots in shot_list:
        counts, p1 = run_shots(qc, shots, backend)
        print(f"{shots:>8} | {str(counts):>28} | {p1:>8.4f} | {abs(p1 - 0.5):>10.4f}")

    print("\nObservation: as shot count increases, |P - 0.5| shrinks, "
          "illustrating the Law of Large Numbers / shot-noise scaling (~1/sqrt(N)).")
