"""
Tutorial 9 - Exercise 3 (Hard)
Measure a Bell pair in the Hadamard (X) basis instead of the computational
(Z) basis and explain the resulting correlation pattern.
Also compares against a CLASSICAL correlated source to show why the X-basis
correlation is a signature of entanglement.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "output", "T09_hard")
os.makedirs(OUT, exist_ok=True)

lines = []
def log(s=""):
    print(s)
    lines.append(str(s))

SHOTS = 1024
OUTCOMES = ["00", "01", "10", "11"]
sim = AerSimulator()

def bell_state(name):
    qc = QuantumCircuit(2, name=name)
    if name in ("Psi+", "Psi-"):
        qc.x(1)
    if name in ("Phi-", "Psi-"):
        qc.x(0)
    qc.h(0)
    qc.cx(0, 1)
    return qc

def measure_in(qc, basis):
    """basis is a 2-char string for (q0, q1): 'Z' = computational,
    'X' = Hadamard basis (apply H before measuring)."""
    m = qc.copy()
    for q, b in enumerate(basis):
        if b == "X":
            m.h(q)
    m.measure_all()
    return m

def run(qc, shots=SHOTS, seed=9):
    r = sim.run(transpile(qc, sim), shots=shots, seed_simulator=seed).result()
    return r.get_counts()

def correlation(counts):
    """E = P(same) - P(different); +1 perfect agreement, -1 perfect
    disagreement, 0 no correlation."""
    n = sum(counts.values())
    same = counts.get("00", 0) + counts.get("11", 0)
    return (2 * same - n) / n

log("=" * 70)
log(" TUTORIAL 9 | EXERCISE 3 (HARD): Bell Pairs in the Hadamard Basis")
log("=" * 70)

# ---------- Part A: Phi+ in Z vs X basis, with circuits ----------
log("\n[A] Phi+ measured in the Z basis vs the X (Hadamard) basis")
phi = bell_state("Phi+")
zz_c = measure_in(phi, "ZZ")
xx_c = measure_in(phi, "XX")
log("\nZ-basis circuit:")
log(zz_c.draw(output="text"))
log("\nX-basis circuit (H on both qubits before measurement):")
log(xx_c.draw(output="text"))
cz, cx = run(zz_c), run(xx_c)
log(f"\nZ basis counts : {dict(sorted(cz.items()))}   E_ZZ = {correlation(cz):+.3f}")
log(f"X basis counts : {dict(sorted(cx.items()))}   E_XX = {correlation(cx):+.3f}")
log("-> Phi+ = (|++> + |-->)/sqrt(2): the qubits agree in BOTH bases.")

# ---------- Part B: all four Bell states, three basis settings ----------
log("\n[B] Correlation of all four Bell states in different bases")
settings = ["ZZ", "XX", "ZX"]
table = {}
hist = {}
for name in ["Phi+", "Phi-", "Psi+", "Psi-"]:
    table[name] = {}
    for s in settings:
        c = run(measure_in(bell_state(name), s))
        table[name][s] = correlation(c)
        if s == "XX":
            hist[name] = c
log(f"\n{'State':<8}{'E_ZZ':>10}{'E_XX':>10}{'E_ZX':>10}   X-basis counts")
log("-" * 70)
for name in table:
    t = table[name]
    log(f"{name:<8}{t['ZZ']:>+10.3f}{t['XX']:>+10.3f}{t['ZX']:>+10.3f}   "
        f"{dict(sorted(hist[name].items()))}")

log("\nReading the table:")
log("  * Phi+ : agree in Z (+1), agree in X (+1)")
log("  * Phi- : agree in Z (+1), DISAGREE in X (-1)  <- the minus sign shows up")
log("  * Psi+ : disagree in Z (-1), agree in X (+1)")
log("  * Psi- : disagree in Z (-1), disagree in X (-1)  (anti-correlated in every basis)")
log("  * Mixed bases (Z on one, X on the other): E ~ 0, no correlation at all.")
log("  * Phi+/Phi- looked identical in Exercise 2 (Z basis); the X basis")
log("    tells them apart. Same for Psi+/Psi-.")

# ---------- Part C: classical correlated source for comparison ----------
log("\n[C] Classical look-alike: a source that sends |00> or |11> at random")
log("    (50/50 classical mixture - no entanglement, no superposition)")
half = SHOTS // 2
classical = {}
for basis in ["ZZ", "XX"]:
    tot = {}
    for seed, prep in [(1, "00"), (2, "11")]:
        qc = QuantumCircuit(2)
        if prep == "11":
            qc.x([0, 1])
        c = run(measure_in(qc, basis), shots=half, seed=seed)
        for k, v in c.items():
            tot[k] = tot.get(k, 0) + v
    classical[basis] = tot
    log(f"    {basis} basis counts : {dict(sorted(tot.items()))}   "
        f"E = {correlation(tot):+.3f}")
log("-> The classical mixture copies Phi+ perfectly in the Z basis (E=+1),")
log("   but in the X basis the correlation vanishes (E~0).")
log("   Phi+ stays perfectly correlated (E=+1) in X too. Correlation that")
log("   survives a change of basis is the fingerprint of entanglement.")

# ---------- Plots ----------
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
for ax, counts, title in [(axes[0], cz, "Phi+ in Z basis"),
                          (axes[1], cx, "Phi+ in X (Hadamard) basis")]:
    vals = [counts.get(o, 0) for o in OUTCOMES]
    b = ax.bar(OUTCOMES, vals, color="#2a9d8f")
    for bar, v in zip(b, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 5, str(v), ha="center")
    ax.set_title(title)
    ax.set_xlabel("Outcome (q1 q0)")
    ax.set_ylabel("Counts")
    ax.set_ylim(0, 620)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "T09_hard_phiplus_Z_vs_X.png"), dpi=150)
plt.close()

fig, ax = plt.subplots(figsize=(9, 4.5))
names = list(table.keys())
x = np.arange(len(names))
w = 0.26
for i, (s, col) in enumerate(zip(settings, ["#264653", "#e76f51", "#bbbbbb"])):
    ax.bar(x + (i - 1) * w, [table[n][s] for n in names], w, label=f"E_{s}", color=col)
ax.axhline(0, color="black", lw=0.8)
ax.set_xticks(x)
ax.set_xticklabels(names)
ax.set_ylim(-1.2, 1.2)
ax.set_ylabel("Correlation E = P(same) - P(diff)")
ax.set_title("Bell-state correlations by measurement basis")
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUT, "T09_hard_correlations.png"), dpi=150)
plt.close()

fig, ax = plt.subplots(figsize=(6, 4))
labels = ["Z basis", "X basis"]
ent = [correlation(cz), correlation(cx)]
cla = [correlation(classical["ZZ"]), correlation(classical["XX"])]
x = np.arange(2)
ax.bar(x - 0.18, ent, 0.36, label="Phi+ (entangled)", color="#2a9d8f")
ax.bar(x + 0.18, cla, 0.36, label="Classical 00/11 mixture", color="#e9c46a")
ax.axhline(0, color="black", lw=0.8)
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylim(-0.2, 1.2)
ax.set_ylabel("Correlation E")
ax.set_title("Entangled vs classical correlation")
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUT, "T09_hard_entangled_vs_classical.png"), dpi=150)
plt.close()

with open(os.path.join(OUT, "T09_hard_output.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\nAll outputs saved to: {OUT}")
