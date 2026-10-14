"""
Tutorial 9 - Exercise 1 (Easy)
Construct the Phi+ Bell state and confirm through a 1024-shot simulation
that only '00' and '11' outcomes occur.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "output", "T09_easy")
os.makedirs(OUT, exist_ok=True)

lines = []
def log(s=""):
    print(s)
    lines.append(str(s))

SHOTS = 1024

log("=" * 60)
log(" TUTORIAL 9 | EXERCISE 1 (EASY): Phi+ Bell State")
log("=" * 60)

# 1. Build the Phi+ circuit: H on q0, then CNOT q0 -> q1
bell = QuantumCircuit(2, name="Phi+")
bell.h(0)
bell.cx(0, 1)

# 2. Statevector check (before measurement)
sv = Statevector.from_instruction(bell)
log("\n[1] Statevector of Phi+ = (|00> + |11>)/sqrt(2)")
for idx, amp in enumerate(sv.data):
    label = format(idx, "02b")
    log(f"    |{label}> : amplitude = {amp.real:+.4f}{amp.imag:+.4f}j   "
        f"probability = {abs(amp)**2:.4f}")

# 3. Add measurement and simulate
qc = bell.copy()
qc.measure_all()
log("\n[2] Circuit:")
log(qc.draw(output="text"))

sim = AerSimulator()
result = sim.run(transpile(qc, sim), shots=SHOTS, seed_simulator=9).result()
counts = dict(sorted(result.get_counts().items()))

log(f"\n[3] Measurement counts ({SHOTS} shots):")
log(f"    {'Outcome':<10}{'Count':>8}{'Probability':>14}")
for k in ["00", "01", "10", "11"]:
    c = counts.get(k, 0)
    log(f"    {k:<10}{c:>8}{c / SHOTS:>14.4f}")

# 4. Verification
allowed = {"00", "11"}
forbidden = {k: v for k, v in counts.items() if k not in allowed}
log("\n[4] Verification:")
log(f"    Outcomes observed      : {sorted(counts.keys())}")
log(f"    Only '00' and '11'?    : {'YES' if not forbidden else 'NO'}")
log(f"    '01' + '10' counts     : {sum(forbidden.values())}")
log(f"    Qubits always agree    : {'YES' if not forbidden else 'NO'} "
    f"(perfect correlation)")
log(f"    Split 00 : 11          : {counts.get('00', 0)} : {counts.get('11', 0)} "
    f"(~50:50 expected)")

# 5. Save histogram
fig, ax = plt.subplots(figsize=(6, 4))
keys = ["00", "01", "10", "11"]
vals = [counts.get(k, 0) for k in keys]
bars = ax.bar(keys, vals, color=["#2a9d8f", "#cccccc", "#cccccc", "#2a9d8f"])
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 5, str(v), ha="center")
ax.set_title(f"Phi+ Bell State - {SHOTS} shots")
ax.set_xlabel("Measured outcome (q1 q0)")
ax.set_ylabel("Counts")
ax.set_ylim(0, max(vals) * 1.15)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "T09_easy_histogram.png"), dpi=150)
plt.close()

# 6. Save circuit diagram
try:
    qc.draw(output="mpl").savefig(os.path.join(OUT, "T09_easy_circuit.png"), dpi=150)
    log("\nSaved: T09_easy_circuit.png")
except Exception as e:
    log(f"\n(circuit image skipped: {e})")

with open(os.path.join(OUT, "T09_easy_output.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\nAll outputs saved to: {OUT}")
