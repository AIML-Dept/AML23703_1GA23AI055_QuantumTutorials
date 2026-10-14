"""
Tutorial 10 - Exercise 1 (Easy)
Implement the superdense coding circuit for the message '00'
and verify correct decoding.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "output", "T10_easy")
os.makedirs(OUT, exist_ok=True)

lines = []
def log(s=""):
    print(s)
    lines.append(str(s))

SHOTS = 1024
MESSAGE = "00"

def show_state(label, qc):
    sv = Statevector.from_instruction(qc)
    terms = [f"{a.real:+.3f}|{format(i, '02b')}>" for i, a in enumerate(sv.data)
             if abs(a) > 1e-9]
    log(f"    {label:<34}: {'  '.join(terms)}")

log("=" * 64)
log(" TUTORIAL 10 | EXERCISE 1 (EASY): Superdense Coding, message '00'")
log("=" * 64)
log("Roles: q0 = Alice's qubit (encoded and sent), q1 = Bob's qubit")

# Step 1: shared entangled pair (prepared before the message is chosen)
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
log("\n[1] State after each stage (Statevector, |q1 q0>):")
show_state("After H + CNOT (shared Phi+)", qc)

# Step 2: Alice encodes '00' -> identity (no gate)
qc.barrier()
qc.id(0)
show_state("After Alice encodes '00' (I)", qc)

# Step 3: Alice sends q0 to Bob; Bob decodes with CNOT then H
qc.barrier()
qc.cx(0, 1)
qc.h(0)
show_state("After Bob's CNOT + H (decode)", qc)

qc.measure_all()
log("\n[2] Full circuit:")
log(qc.draw(output="text"))

sim = AerSimulator()
counts = sim.run(transpile(qc, sim), shots=SHOTS, seed_simulator=10).result().get_counts()
counts = dict(sorted(counts.items()))
decoded = max(counts, key=counts.get)

log(f"\n[3] Measurement counts ({SHOTS} shots): {counts}")
log("\n[4] Verification:")
log(f"    Message sent by Alice    : {MESSAGE}")
log(f"    Message decoded by Bob   : {decoded}")
log(f"    Correct decodes          : {counts.get(MESSAGE, 0)} / {SHOTS}")
log(f"    Decoding accuracy        : {100 * counts.get(MESSAGE, 0) / SHOTS:.2f}%")
log(f"    Decoded correctly?       : {'YES' if decoded == MESSAGE else 'NO'}")
log("    Classical bits delivered : 2   |   Qubits sent by Alice : 1")

# Histogram
fig, ax = plt.subplots(figsize=(6, 4))
keys = ["00", "01", "10", "11"]
vals = [counts.get(k, 0) for k in keys]
bars = ax.bar(keys, vals, color=["#2a9d8f" if k == MESSAGE else "#cccccc" for k in keys])
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 10, str(v), ha="center")
ax.set_title(f"Superdense coding - message '{MESSAGE}' ({SHOTS} shots)")
ax.set_xlabel("Decoded message (Bob's measurement)")
ax.set_ylabel("Counts")
ax.set_ylim(0, SHOTS * 1.12)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "T10_easy_histogram.png"), dpi=150)
plt.close()

try:
    qc.draw(output="mpl").savefig(os.path.join(OUT, "T10_easy_circuit.png"),
                                  dpi=150, bbox_inches="tight")
    log("\nSaved: T10_easy_circuit.png")
except Exception as e:
    log(f"\n(circuit image skipped: {e})")

with open(os.path.join(OUT, "T10_easy_output.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\nAll outputs saved to: {OUT}")
