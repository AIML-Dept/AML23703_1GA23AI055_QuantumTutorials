"""
Tutorial 10 - Exercise 4 (Real-world)
Compare the classical bandwidth requirement with superdense-coded
transmission for a hypothetical 100-message communication session.
Each message is a 2-bit symbol ('00', '01', '10' or '11').
All 100 messages are actually sent through the simulated protocol and
decoded, on an ideal channel and on a noisy channel (bit-flip p = 0.05).
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
OUT = os.path.join(BASE, "output", "T10_realworld")
os.makedirs(OUT, exist_ok=True)

lines = []
def log(s=""):
    print(s)
    lines.append(str(s))

N_MESSAGES = 100
BITS_PER_MSG = 2
NOISE_P = 0.05
rng = np.random.default_rng(10)
sim = AerSimulator()

def superdense_circuit(message, flip_p=0.0):
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)                    # pre-shared ebit
    if message[0] == "1":
        qc.x(0)
    if message[1] == "1":
        qc.z(0)
    if flip_p > 0:                 # channel noise on the sent qubit
        qc.append(pauli_error([("X", flip_p), ("I", 1 - flip_p)]), [0])
    qc.cx(0, 1)
    qc.h(0)
    qc.measure_all()
    return qc

CIRCUITS = {}
def compiled(message, flip_p):
    key = (message, flip_p)
    if key not in CIRCUITS:
        CIRCUITS[key] = transpile(superdense_circuit(message, flip_p), sim)
    return CIRCUITS[key]

def send_sessions(messages, flip_p, n_sessions, seed):
    """Send the whole message list n_sessions times (1 shot per message per
    session). Returns a list of sessions, each a list of Bob's decoded messages."""
    sessions = [[None] * len(messages) for _ in range(n_sessions)]
    for k, m in enumerate(["00", "01", "10", "11"]):
        idx = [i for i, x in enumerate(messages) if x == m]
        if not idx:
            continue
        mem = sim.run(compiled(m, flip_p), shots=len(idx) * n_sessions,
                      memory=True, seed_simulator=seed + k).result().get_memory()
        for r in range(n_sessions):
            chunk = mem[r * len(idx):(r + 1) * len(idx)]
            for i, out in zip(idx, chunk):
                sessions[r][i] = out
    return sessions

log("=" * 72)
log(" TUTORIAL 10 | EXERCISE 4 (REAL-WORLD): 100-Message Bandwidth Study")
log("=" * 72)

messages = [rng.choice(["00", "01", "10", "11"]) for _ in range(N_MESSAGES)]
uniq, cnt = np.unique(messages, return_counts=True)
log(f"\nSession: {N_MESSAGES} random 2-bit messages "
    f"= {N_MESSAGES * BITS_PER_MSG} classical bits of information")
log("Message mix : " + ", ".join(f"'{u}' x {c}" for u, c in zip(uniq, cnt)))
log("First 10    : " + " ".join(messages[:10]))

# ---------- Run the session through the protocol ----------
N_REPEAT = 200
ideal = send_sessions(messages, 0.0, 1, seed=1000)[0]
noisy_all = send_sessions(messages, NOISE_P, N_REPEAT, seed=2000)
noisy = noisy_all[0]
ok_ideal = sum(a == b for a, b in zip(messages, ideal))
ok_noisy = sum(a == b for a, b in zip(messages, noisy))
bit_err_noisy = sum((a[0] != b[0]) + (a[1] != b[1]) for a, b in zip(messages, noisy))
wrong = np.array([sum(a != b for a, b in zip(messages, sess)) for sess in noisy_all])

log("\n[1] Simulated transmission of the full session")
log(f"    Ideal channel            : {ok_ideal}/{N_MESSAGES} messages decoded correctly")
log(f"    Bit-flip p = {NOISE_P} (session 1): {ok_noisy}/{N_MESSAGES} messages decoded correctly, "
    f"{bit_err_noisy} bit errors out of {N_MESSAGES * BITS_PER_MSG}")
log("    First 10 decoded (ideal): " + " ".join(ideal[:10]))
log("    First 10 decoded (noisy): " + " ".join(noisy[:10]))
log(f"\n    Noisy session repeated {N_REPEAT} times (p = {NOISE_P}):")
log(f"    Wrong messages per session : mean {wrong.mean():.2f}, "
    f"min {wrong.min()}, max {wrong.max()}  (expected {N_MESSAGES * NOISE_P:.0f})")
log(f"    Sessions with zero errors  : {(wrong == 0).sum()} / {N_REPEAT}")

# ---------- Bandwidth accounting ----------
classical_uses = N_MESSAGES * BITS_PER_MSG       # 1 bit per channel use
sdc_live = N_MESSAGES                             # 1 qubit per message
sdc_preshare = N_MESSAGES                         # 1 ebit (Bob's half) per message
sdc_total = sdc_live + sdc_preshare

log("\n[2] Bandwidth comparison for the session")
hdr = f"{'Quantity':<44}{'Classical':>12}{'Superdense':>13}"
log(hdr)
log("-" * len(hdr))
rows = [
    ("Information delivered (bits)", N_MESSAGES * BITS_PER_MSG, N_MESSAGES * BITS_PER_MSG),
    ("Carriers sent during the session", f"{classical_uses} bits", f"{sdc_live} qubits"),
    ("Bits delivered per carrier sent", "1", "2"),
    ("Pre-shared resource needed beforehand", "none", f"{sdc_preshare} ebits"),
    ("Total carriers incl. pre-sharing", classical_uses, sdc_total),
]
for name, a, b in rows:
    log(f"{name:<44}{str(a):>12}{str(b):>13}")
log("-" * len(hdr))
saving = 100 * (classical_uses - sdc_live) / classical_uses
log(f"Channel uses during the session: {classical_uses} -> {sdc_live} "
    f"({saving:.0f}% fewer)")
log(f"Total including ebit distribution: {classical_uses} -> {sdc_total} (no net saving)")

log("\nSummary:")
log("  * During the session superdense coding halves the traffic: 100 qubits")
log("    carry the 200 bits, because each qubit delivers 2 bits.")
log("  * The cost is paid in advance: 100 entangled pairs must be shared")
log("    before the session, so the total number of carriers is still 200.")
log("  * The gain is useful when the session channel is the bottleneck and")
log("    ebits can be distributed earlier, e.g. during off-peak time.")
log(f"  * Real channels add noise: at p = {NOISE_P}, about {wrong.mean():.1f} of "
    f"{N_MESSAGES} messages")
log("    arrive wrong per session on average, so error correction would be needed.")

# ---------- Plots ----------
fig, axes = plt.subplots(1, 3, figsize=(15, 4.4))
labels = ["Classical", "Superdense"]
live = [classical_uses, sdc_live]
pre = [0, sdc_preshare]
axes[0].bar(labels, live, color="#2a9d8f", label="Sent during session")
axes[0].bar(labels, pre, bottom=live, color="#a8dadc",
            label="Ebits pre-shared beforehand")
for i, (l, p) in enumerate(zip(live, pre)):
    axes[0].text(i, l / 2, str(l), ha="center", color="white", fontweight="bold")
    if p:
        axes[0].text(i, l + p / 2, str(p), ha="center")
axes[0].set_ylabel("Carriers transmitted")
axes[0].set_title(f"{N_MESSAGES}-message session (200 bits of information)")
axes[0].set_ylim(0, 240)
axes[0].legend(loc="upper right", fontsize=8)

n = np.arange(0, 1001, 50)
axes[1].plot(n, 2 * n, marker="o", ms=3, color="#264653", label="Classical: 2 bits per message")
axes[1].plot(n, n, marker="s", ms=3, color="#2a9d8f", label="Superdense: 1 qubit per message")
axes[1].axvline(N_MESSAGES, ls=":", color="grey")
axes[1].text(N_MESSAGES + 15, 1700, f"this session\n(N = {N_MESSAGES})", fontsize=8)
axes[1].set_xlabel("Number of 2-bit messages")
axes[1].set_ylabel("Channel uses during session")
axes[1].set_title("Session traffic scaling")
axes[1].grid(alpha=0.3)
axes[1].legend(fontsize=8)
bins = np.arange(wrong.min(), wrong.max() + 2) - 0.5
axes[2].hist(wrong, bins=bins, color="#e76f51", edgecolor="white")
axes[2].axvline(wrong.mean(), ls="--", color="black", label=f"mean = {wrong.mean():.2f}")
axes[2].set_xlabel("Wrong messages in a 100-message session")
axes[2].set_ylabel("Number of sessions")
axes[2].set_title(f"Noisy channel (p = {NOISE_P}), {N_REPEAT} sessions")
axes[2].legend(fontsize=8)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "T10_realworld_bandwidth.png"), dpi=150)
plt.close()

with open(os.path.join(OUT, "T10_realworld_output.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\nAll outputs saved to: {OUT}")
