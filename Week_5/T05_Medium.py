"""
Tutorial 5 - MEDIUM Exercise
Measure a qubit in the X-basis (apply H before measurement) after
preparing |+> and |-> states, and interpret the results.
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def prepare_plus():
    qc = QuantumCircuit(1, 1)
    qc.h(0)             # |0> -> |+>
    return qc


def prepare_minus():
    qc = QuantumCircuit(1, 1)
    qc.x(0)             # |0> -> |1>
    qc.h(0)             # |1> -> |->
    return qc


def measure_in_x_basis(qc):
    qc.h(0)              # rotate X-basis -> Z-basis
    qc.measure(0, 0)
    return qc


if __name__ == "__main__":
    backend = AerSimulator()
    shots = 2000

    for label, prep_fn in [("|+>", prepare_plus), ("|->", prepare_minus)]:
        qc = prep_fn()
        qc = measure_in_x_basis(qc)
        tqc = transpile(qc, backend)
        counts = backend.run(tqc, shots=shots).result().get_counts()
        print(f"State {label} measured in X-basis over {shots} shots -> counts: {counts}")

    print("\nInterpretation:")
    print("- |+> measured in the X-basis should collapse (near) deterministically to outcome '0'.")
    print("- |-> measured in the X-basis should collapse (near) deterministically to outcome '1'.")
    print("- Any small deviation from 100%/0% is purely simulator shot noise, "
          "since these are exact eigenstates of the X operator.")
