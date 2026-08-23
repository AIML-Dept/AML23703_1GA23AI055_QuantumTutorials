"""
Tutorial 5 - HARD Exercise
Perform partial measurement on one qubit of a 2-qubit Bell pair and
analyse the resulting state of the unmeasured qubit.
"""

import matplotlib
matplotlib.use("Agg")

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector, partial_trace
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram


def build_bell_pair():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    return qc


if __name__ == "__main__":
    qc_theory = QuantumCircuit(2)
    qc_theory.h(0)
    qc_theory.cx(0, 1)
    full_state = Statevector.from_instruction(qc_theory)
    print("Full Bell state |Phi+>:", full_state)

    reduced_before = partial_trace(full_state, [0])
    print("\nReduced density matrix of qubit 1 BEFORE measuring qubit 0"
          " (maximally mixed -> no definite value):")
    print(np.round(reduced_before.data, 3))

    outcome, collapsed = full_state.measure([0])
    print(f"\nMeasured qubit 0 (statevector simulation) -> outcome = {outcome}")
    reduced_after = partial_trace(collapsed, [0])
    print("Reduced density matrix of qubit 1 AFTER measuring qubit 0"
          " (now a pure, definite state):")
    print(np.round(reduced_after.data, 3))

    backend = AerSimulator()
    qc = build_bell_pair()
    qc.measure(0, 0)
    qc.measure(1, 1)

    fig = qc.draw('mpl')
    fig.savefig("T05_Hard_circuit.png", dpi=150, bbox_inches="tight")

    tqc = transpile(qc, backend)
    counts = backend.run(tqc, shots=2000).result().get_counts()
    print(f"\nJoint measurement counts over 2000 shots (bit order c1 c0): {counts}")

    hist_fig = plot_histogram(counts, title="Bell pair joint measurement")
    hist_fig.savefig("T05_Hard_hist.png", dpi=150, bbox_inches="tight")

    print("\nInterpretation:")
    print("- Only outcomes '00' and '11' appear (up to shot noise); '01'/'10' essentially never occur.")
    print("- Measuring qubit 0 alone collapses qubit 1 to match it exactly, "
          "even though qubit 1 was never directly measured.")
    print("- This is the hallmark of entanglement: the reduced state goes from "
          "maximally mixed to pure the instant the partner qubit is measured.")
