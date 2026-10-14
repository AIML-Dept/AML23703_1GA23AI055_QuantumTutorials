"""
Tutorial 9 - Exercise 2 (Medium)
Construct all four Bell states and tabulate the measurement outcome
distributions for comparison.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "output", "T09_medium")
os.makedirs(OUT, exist_ok=True)

lines = []
def log(s=""):
    print(s)
    lines.append(str(s))

SHOTS = 1024
OUTCOMES = ["00", "01", "10", "11"]

def bell_state(name):
    """Return the 2-qubit circuit (no measurement) that prepares a Bell state.
    Recipe: optional X on q1 (Psi), optional X on q0 (minus sign),
    then H on q0 and CNOT q0 -> q1."""
    qc = QuantumCircuit(2, name=name)
    if name in ("Psi+", "Psi-"):
        qc.x(1)          # flip target -> |01>/|10> family
    if name in ("Phi-", "Psi-"):
        qc.x(0)          # |1> before H -> minus sign
    qc.h(0)
    qc.cx(0, 1)
    return qc

FORMULA = {
    "Phi+": "(|00> + |11>)/sqrt(2)",
    "Phi-": "(|00> - |11>)/sqrt(2)",
    "Psi+": "(|01> + |10>)/sqrt(2)",
    "Psi-": "(|01> - |10>)/sqrt(2)",
}

log("=" * 66)
log(" TUTORIAL 9 | EXERCISE 2 (MEDIUM): All Four Bell States")
log("=" * 66)

sim = AerSimulator()
all_counts = {}

for name in ["Phi+", "Phi-", "Psi+", "Psi-"]:
    bell = bell_state(name)
    sv = Statevector.from_instruction(bell)

    log(f"\n--- {name} = {FORMULA[name]} ---")
    log(bell.draw(output="text"))
    amps = "  ".join(f"|{format(i,'02b')}>:{a.real:+.3f}" for i, a in enumerate(sv.data))
    log(f"Statevector amplitudes : {amps}")

    qc = bell.copy()
    qc.measure_all()
    res = sim.run(transpile(qc, sim), shots=SHOTS, seed_simulator=9).result()
    counts = res.get_counts()
    all_counts[name] = counts

    # parity correlation <ZZ> = P(same) - P(different)
    same = counts.get("00", 0) + counts.get("11", 0)
    diff = counts.get("01", 0) + counts.get("10", 0)
    zz = (same - diff) / SHOTS
    log(f"Counts                 : {dict(sorted(counts.items()))}")
    log(f"<ZZ> correlation       : {zz:+.3f}  "
        f"({'qubits AGREE' if zz > 0 else 'qubits DISAGREE'})")

# ---- Comparison table ----
log("\n" + "=" * 66)
log(f" COMPARISON TABLE  ({SHOTS} shots each, counts and probability)")
log("=" * 66)
header = f"{'State':<8}" + "".join(f"{o:>12}" for o in OUTCOMES) + f"{'<ZZ>':>10}"
log(header)
log("-" * len(header))
for name, counts in all_counts.items():
    row = f"{name:<8}"
    for o in OUTCOMES:
        c = counts.get(o, 0)
        row += f"{c:>5} ({c/SHOTS:.2f})"
    same = counts.get("00", 0) + counts.get("11", 0)
    row += f"{(2*same - SHOTS)/SHOTS:>+10.3f}"
    log(row)

log("\nKey observations:")
log("  * Phi+ and Phi- both give only 00/11 -> identical in the Z basis.")
log("  * Psi+ and Psi- both give only 01/10 -> identical in the Z basis.")
log("  * The +/- relative phase is invisible to a Z-basis measurement;")
log("    it only shows up in a different basis (see Exercise 3).")
log("  * Psi- prints as -|01> + |10>: this is (|01> - |10>)/sqrt(2) times a")
log("    global phase of -1, which has no physical effect.")

# ---- Grouped bar chart ----
fig, ax = plt.subplots(figsize=(9, 4.8))
x = np.arange(len(OUTCOMES))
w = 0.2
colors = ["#264653", "#2a9d8f", "#e9c46a", "#e76f51"]
for i, (name, counts) in enumerate(all_counts.items()):
    vals = [counts.get(o, 0) for o in OUTCOMES]
    ax.bar(x + (i - 1.5) * w, vals, w, label=name, color=colors[i])
ax.set_xticks(x)
ax.set_xticklabels(OUTCOMES)
ax.set_xlabel("Measured outcome (q1 q0)")
ax.set_ylabel("Counts")
ax.set_title(f"Measurement distributions of the four Bell states ({SHOTS} shots)")
ax.legend(title="Bell state")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "T09_medium_comparison.png"), dpi=150)
plt.close()

# ---- Table as an image (handy for the report) ----
fig, ax = plt.subplots(figsize=(8, 2.2))
ax.axis("off")
cell = [[n] + [str(all_counts[n].get(o, 0)) for o in OUTCOMES] + [FORMULA[n]]
        for n in all_counts]
t = ax.table(cellText=cell, colLabels=["State"] + OUTCOMES + ["Form"],
             loc="center", cellLoc="center",
             colWidths=[0.12, 0.1, 0.1, 0.1, 0.1, 0.38])
t.auto_set_font_size(False)
t.set_fontsize(10)
t.scale(1, 1.6)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "T09_medium_table.png"), dpi=150)
plt.close()

with open(os.path.join(OUT, "T09_medium_output.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\nAll outputs saved to: {OUT}")
