"""
Tutorial 5 - REAL-WORLD Exercise
Use repeated measurement statistics to estimate an unknown rotation
angle applied to a qubit (simple quantum state tomography).
"""

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

rng = np.random.default_rng(seed=42)
TRUE_THETA = rng.uniform(0, np.pi)   # radians, "unknown" to the estimator


def prepare_unknown_state():
    qc = QuantumCircuit(1, 1)
    qc.ry(TRUE_THETA, 0)
    return qc


def estimate_theta(shots, backend):
    qc = prepare_unknown_state()
    qc.measure(0, 0)
    tqc = transpile(qc, backend)
    counts = backend.run(tqc, shots=shots).result().get_counts()

    p1 = counts.get('1', 0) / shots
    p1_clipped = min(max(p1, 0.0), 1.0)
    theta_est = 2 * np.arcsin(np.sqrt(p1_clipped))
    return theta_est, p1, counts


if __name__ == "__main__":
    backend = AerSimulator()

    print(f"{'Shots':>8} | {'P(|1>) est.':>12} | {'theta est. (rad)':>16} | {'abs error (rad)':>16}")
    print("-" * 65)
    for shots in [100, 1000, 10000, 50000]:
        theta_est, p1, counts = estimate_theta(shots, backend)
        err = abs(theta_est - TRUE_THETA)
        print(f"{shots:>8} | {p1:>12.4f} | {theta_est:>16.4f} | {err:>16.4f}")

    print(f"\nTrue theta (revealed for verification): {TRUE_THETA:.4f} rad "
          f"({np.degrees(TRUE_THETA):.2f} deg)")
    print("Observation: the estimate of theta gets closer to the true value "
          "as shot count increases, same statistical-convergence principle as Exercise 1.")
