"""
Tutorial 10 - Exercise 3 (Hard)
Introduce a bit-flip error on the transmitted qubit (simulated channel
noise) and analyse the impact on decoding accuracy.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import pauli_error

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "output", "T10_hard")
os.makedirs(OUT, exist_ok=True)

lines = []
def log(s=""):
    print(s)
    lines.append(str(s))

SHOTS = 2048
MESSAGES = ["00", "01", "10", "11"]
sim = AerSimulator()

def superdense_circuit(message, flip_p=0.0, certain_flip=False):
    """Alice's qubit q0 travels to Bob through a channel that applies
    an X (bit-flip) error with probability flip_p."""
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)                       # shared Phi+ pair
    if message[0] == "1":
        qc.x(0)                       # Alice's encoding
    if message[1] == "1":
        qc.z(0)
    qc.barrier(label="channel")
    if certain_flip:
        qc.x(0)                       # error happens every time
    elif flip_p > 0:
        qc.append(pauli_error([("X", flip_p), ("I", 1 - flip_p)]), [0])
    qc.barrier()
    qc.cx(0, 1)                       # Bob's Bell-basis decoding
    qc.h(0)
    qc.measure_all()
    return qc

def run(qc, seed):
    return sim.run(transpile(qc, sim), shots=SHOTS,
                   seed_simulator=seed).result().get_counts()

log("=" * 72)
log(" TUTORIAL 10 | EXERCISE 3 (HARD): Bit-flip Noise on the Sent Qubit")
log("=" * 72)

# ---------- Part A: a certain bit flip ----------
log("\n[A] Channel ALWAYS applies X to Alice's qubit (p = 1)")
log(superdense_circuit("01", certain_flip=True).draw(output="text"))
log(f"\n{'Sent':<8}{'Decoded counts':<26}{'Bob reads':<11}Effect")
log("-" * 60)
for m in MESSAGES:
    c = dict(sorted(run(superdense_circuit(m, certain_flip=True), seed=10).items()))
    got = max(c, key=c.get)
    eff = "first bit flipped" if got[0] != m[0] and got[1] == m[1] else "other"
    log(f"{m:<8}{str(c):<26}{got:<11}{eff}")
log("-> An X error acts like an extra X from Alice: it flips the FIRST bit")
log("   (the bit carried by X) and leaves the second bit (carried by Z) alone.")

# ---------- Part B: probabilistic bit-flip channel ----------
log("\n[B] Bit-flip channel with probability p (Qiskit Aer pauli_error)")
P_VALUES = [0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5]
acc = {m: [] for m in MESSAGES}
bit_err = {"first": [], "second": []}
for k, p in enumerate(P_VALUES):
    e1 = e2 = 0
    for j, m in enumerate(MESSAGES):
        c = run(superdense_circuit(m, flip_p=p), seed=100 + 10 * k + j)
        acc[m].append(c.get(m, 0) / SHOTS)
        for out, n in c.items():
            e1 += n * (out[0] != m[0])
            e2 += n * (out[1] != m[1])
    bit_err["first"].append(e1 / (SHOTS * 4))
    bit_err["second"].append(e2 / (SHOTS * 4))

log(f"\n{'p':>5}" + "".join(f"{'acc ' + m:>10}" for m in MESSAGES)
    + f"{'avg':>9}{'theory':>9}{'BER b1':>9}{'BER b2':>9}")
log("-" * 82)
avg = []
for k, p in enumerate(P_VALUES):
    a = np.mean([acc[m][k] for m in MESSAGES])
    avg.append(a)
    log(f"{p:>5.2f}" + "".join(f"{acc[m][k]:>10.3f}" for m in MESSAGES)
        + f"{a:>9.3f}{1 - p:>9.3f}{bit_err['first'][k]:>9.3f}{bit_err['second'][k]:>9.3f}")
log("(acc = fraction decoded correctly, theory = 1 - p,")
log(" BER b1 / b2 = error rate of the first / second message bit)")
log("\nObservations:")
log("  * Accuracy falls linearly as 1 - p for every message.")
log("  * Only the first bit is ever corrupted; the second bit stays error-free.")
log("  * At p = 0.5 the first bit is a coin toss, so only 1 bit of the 2 survives.")

# ---------- Part C: decoding matrix at p = 0.2 ----------
P_SHOW = 0.2
log(f"\n[C] Decoding matrix at p = {P_SHOW} (rows = sent, columns = decoded)")
keys = ["00", "01", "10", "11"]
matrix = []
for j, m in enumerate(MESSAGES):
    c = run(superdense_circuit(m, flip_p=P_SHOW), seed=500 + j)
    matrix.append([c.get(k, 0) for k in keys])
log(f"{'sent':<8}" + "".join(f"{k:>8}" for k in keys))
for m, row in zip(MESSAGES, matrix):
    log(f"{m:<8}" + "".join(f"{v:>8}" for v in row))

# ---------- Plots ----------
fig, ax = plt.subplots(figsize=(7, 4.5))
for m, col in zip(MESSAGES, ["#264653", "#2a9d8f", "#e9c46a", "#e76f51"]):
    ax.plot(P_VALUES, acc[m], marker="o", label=f"sent '{m}'", color=col, alpha=0.85)
ax.plot(P_VALUES, [1 - p for p in P_VALUES], "k--", label="theory 1 - p")
ax.set_xlabel("Bit-flip probability p on transmitted qubit")
ax.set_ylabel("Decoding accuracy")
ax.set_title("Superdense coding under bit-flip channel noise")
ax.set_ylim(0.4, 1.05)
ax.grid(alpha=0.3)
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUT, "T10_hard_accuracy_vs_p.png"), dpi=150)
plt.close()

fig, axes = plt.subplots(1, 2, figsize=(11, 4.3))
axes[0].plot(P_VALUES, bit_err["first"], marker="o", color="#e76f51", label="first bit (X-encoded)")
axes[0].plot(P_VALUES, bit_err["second"], marker="s", color="#2a9d8f", label="second bit (Z-encoded)")
axes[0].set_xlabel("Bit-flip probability p")
axes[0].set_ylabel("Bit error rate")
axes[0].set_title("Which message bit is corrupted?")
axes[0].grid(alpha=0.3)
axes[0].legend()
im = axes[1].imshow(matrix, cmap="Oranges")
for i in range(4):
    for j in range(4):
        axes[1].text(j, i, matrix[i][j], ha="center", va="center",
                     color="white" if matrix[i][j] > SHOTS / 2 else "black")
axes[1].set_xticks(range(4))
axes[1].set_xticklabels(keys)
axes[1].set_yticks(range(4))
axes[1].set_yticklabels(MESSAGES)
axes[1].set_xlabel("Decoded by Bob")
axes[1].set_ylabel("Sent by Alice")
axes[1].set_title(f"Decoding matrix at p = {P_SHOW}")
plt.colorbar(im, ax=axes[1], fraction=0.046)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "T10_hard_bit_errors.png"), dpi=150)
plt.close()

with open(os.path.join(OUT, "T10_hard_output.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\nAll outputs saved to: {OUT}")
