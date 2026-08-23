"""
Tutorial 5 - MEDIUM Exercise
Measure a qubit in the X-basis (apply H before measurement) after
preparing |+> and |-> states, and interpret the results.
"""

import matplotlib
matplotlib.use("Agg")

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram


def prepare_plus():
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    return qc


def prepare_minus():
    qc = QuantumCircuit(1, 1)
    qc.x(0)
    qc.h(0)
    return qc


def measure_in_x_basis(qc):
    qc.h(0)
    qc.measure(0, 0)
    return qc


if __name__ == "__main__":
    backend = AerSimulator()
    shots = 2000

    for label, prep_fn in [("plus", prepare_plus), ("minus", prepare_minus)]:
        qc = prep_fn()
        qc = measure_in_x_basis(qc)

        fig = qc.draw('mpl')
        fig.savefig(f"T05_Medium_circuit_{label}.png", dpi=150, bbox_inches="tight")

        tqc = transpile(qc, backend)
        counts = backend.run(tqc, shots=shots).result().get_counts()
        symbol = "+" if label == "plus" else "-"
        print(f"State |{symbol}> measured in X-basis over {shots} shots -> counts: {counts}")

        hist_fig = plot_histogram(counts, title=f"|{symbol}> in X-basis")
        hist_fig.savefig(f"T05_Medium_hist_{label}.png", dpi=150, bbox_inches="tight")

    print("\nInterpretation:")
    print("- |+> measured in the X-basis should collapse (near) deterministically to outcome '0'.")
    print("- |-> measured in the X-basis should collapse (near) deterministically to outcome '1'.")
    print("- Any small deviation from 100%/0% is purely simulator shot noise, "
          "since these are exact eigenstates of the X operator.")
