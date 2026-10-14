"""
Tutorial 10 - Exercise 2 (Medium)
Implement superdense coding for all four 2-bit messages
('00', '01', '10', '11') and tabulate the decoded results.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "output", "T10_medium")
os.makedirs(OUT, exist_ok=True)

lines = []
def log(s=""):
    print(s)
    lines.append(str(s))

SHOTS = 1024
MESSAGES = ["00", "01", "10", "11"]
GATES = {"00": "I", "01": "Z", "10": "X", "11": "X then Z (ZX)"}
BELL = {"00": "Phi+", "01": "Phi-", "10": "Psi+", "11": "Psi-"}

def encode(qc, message):
    """Alice's encoding on her qubit q0.
    First bit -> X (bit flip), second bit -> Z (phase flip)."""
    if message[0] == "1":
        qc.x(0)
    if message[1] == "1":
        qc.z(0)
    if message == "00":
        qc.id(0)

def superdense_circuit(message):
    qc = QuantumCircuit(2, name=f"SDC_{message}")
    qc.h(0)
    qc.cx(0, 1)            # shared Phi+ pair
    qc.barrier()
    encode(qc, message)    # Alice encodes 2 bits on 1 qubit
    qc.barrier()
    qc.cx(0, 1)            # Bob's Bell-basis measurement:
    qc.h(0)                # CNOT then H, then measure in Z
    return qc

def fmt_state(qc):
    sv = Statevector.from_instruction(qc)
    return "  ".join(f"{a.real:+.3f}|{format(i, '02b')}>"
                     for i, a in enumerate(sv.data) if abs(a) > 1e-9)

log("=" * 72)
log(" TUTORIAL 10 | EXERCISE 2 (MEDIUM): Superdense Coding, all 4 messages")
log("=" * 72)

sim = AerSimulator()
results = {}
for m in MESSAGES:
    # state just after Alice's encoding (before decoding)
    enc = QuantumCircuit(2)
    enc.h(0)
    enc.cx(0, 1)
    encode(enc, m)

    qc = superdense_circuit(m)
    log(f"\n--- Message '{m}' | Alice applies {GATES[m]} ---")
    log(qc.draw(output="text"))
    log(f"State after encoding : {fmt_state(enc)}   (= {BELL[m]})")

    qc.measure_all()
    counts = sim.run(transpile(qc, sim), shots=SHOTS, seed_simulator=10).result().get_counts()
    counts = dict(sorted(counts.items()))
    decoded = max(counts, key=counts.get)
    results[m] = (counts, decoded)
    log(f"Counts               : {counts}")
    log(f"Decoded message      : {decoded}  -> {'CORRECT' if decoded == m else 'WRONG'}")

log("\n" + "=" * 72)
log(f" DECODING TABLE ({SHOTS} shots per message)")
log("=" * 72)
hdr = f"{'Sent':<6}{'Alice gate':<16}{'Bell state':<12}{'Decoded':<9}{'Correct':>9}{'Accuracy':>11}"
log(hdr)
log("-" * len(hdr))
total_ok = 0
for m in MESSAGES:
    counts, decoded = results[m]
    ok = counts.get(m, 0)
    total_ok += ok
    log(f"{m:<6}{GATES[m]:<16}{BELL[m]:<12}{decoded:<9}{ok:>9}{100 * ok / SHOTS:>10.2f}%")
log("-" * len(hdr))
log(f"Overall: {total_ok} / {SHOTS * len(MESSAGES)} shots decoded correctly "
    f"({100 * total_ok / (SHOTS * len(MESSAGES)):.2f}%)")
log("Each message: 2 classical bits delivered by sending 1 qubit.")
log("Note: Psi- prints as -|01> + |10>, i.e. (|01> - |10>)/sqrt(2) times a")
log("global phase of -1, which has no physical effect.")

# 2x2 histograms
fig, axes = plt.subplots(2, 2, figsize=(9, 6.5))
keys = ["00", "01", "10", "11"]
for ax, m in zip(axes.flat, MESSAGES):
    counts, _ = results[m]
    vals = [counts.get(k, 0) for k in keys]
    bars = ax.bar(keys, vals, color=["#2a9d8f" if k == m else "#cccccc" for k in keys])
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 15, str(v), ha="center", fontsize=9)
    ax.set_title(f"Sent '{m}' ({GATES[m]}, {BELL[m]})", fontsize=10)
    ax.set_ylim(0, SHOTS * 1.15)
    ax.set_xlabel("Decoded message")
    ax.set_ylabel("Counts")
fig.suptitle(f"Superdense coding: all four messages ({SHOTS} shots each)")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "T10_medium_all_messages.png"), dpi=150)
plt.close()

# Decoding matrix (sent vs decoded)
fig, ax = plt.subplots(figsize=(5.2, 4.4))
matrix = [[results[m][0].get(k, 0) for k in keys] for m in MESSAGES]
im = ax.imshow(matrix, cmap="Greens")
for i in range(4):
    for j in range(4):
        ax.text(j, i, matrix[i][j], ha="center", va="center",
                color="white" if matrix[i][j] > SHOTS / 2 else "black")
ax.set_xticks(range(4))
ax.set_xticklabels(keys)
ax.set_yticks(range(4))
ax.set_yticklabels(MESSAGES)
ax.set_xlabel("Decoded by Bob")
ax.set_ylabel("Sent by Alice")
ax.set_title("Decoding matrix (counts)")
plt.colorbar(im, ax=ax, fraction=0.046)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "T10_medium_decoding_matrix.png"), dpi=150)
plt.close()

with open(os.path.join(OUT, "T10_medium_output.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\nAll outputs saved to: {OUT}")
