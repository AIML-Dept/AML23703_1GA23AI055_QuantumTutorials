"""
Tutorial 9 - Exercise 4 (Real-world)
Relate Bell-state correlations to Quantum Key Distribution (QKD).
Simulates an entanglement-based protocol (E91 / BBM92 style):
  1. A source sends one qubit of each Phi+ pair to Alice and one to Bob.
  2. Each picks a random basis (Z or X) and measures.
  3. They publicly compare BASES only and keep matching rounds -> shared key.
  4. They sacrifice part of the key to estimate the error rate (QBER).
  5. A CHSH test checks that the pairs are still genuinely entangled.
The run is repeated with an eavesdropper (Eve, intercept-resend attack).
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "output", "T09_realworld")
os.makedirs(OUT, exist_ok=True)

lines = []
def log(s=""):
    print(s)
    lines.append(str(s))

sim = AerSimulator()
rng = np.random.default_rng(9)
N_PAIRS = 2000          # entangled pairs sent
CHSH_SHOTS = 8192       # shots per CHSH setting

# ------------------------------------------------------------------
# Circuit builders (q0 = Alice, q1 = Bob, clbit0 = Alice, clbit1 = Bob)
# ------------------------------------------------------------------
def rotate_to(qc, q, basis):
    """Rotate so that a Z-measurement measures in the requested basis."""
    if basis == "X":
        qc.h(q)

def bb84_circuit(a_basis, b_basis, eve_basis=None):
    qc = QuantumCircuit(2, 3)       # clbit2 = Eve's record
    qc.h(0)
    qc.cx(0, 1)                     # Phi+
    if eve_basis is not None:       # Eve intercepts Bob's qubit
        rotate_to(qc, 1, eve_basis)
        qc.measure(1, 2)
        rotate_to(qc, 1, eve_basis) # resend the state she measured
    rotate_to(qc, 0, a_basis)
    rotate_to(qc, 1, b_basis)
    qc.measure(0, 0)
    qc.measure(1, 1)
    return qc

def run_qkd(with_eve):
    a_bases = rng.choice(["Z", "X"], N_PAIRS)
    b_bases = rng.choice(["Z", "X"], N_PAIRS)
    e_bases = rng.choice(["Z", "X"], N_PAIRS)
    a_bits = np.zeros(N_PAIRS, dtype=int)
    b_bits = np.zeros(N_PAIRS, dtype=int)
    # group rounds by setting so we run few circuits, one shot per round
    combos = {}
    for i in range(N_PAIRS):
        key = (a_bases[i], b_bases[i], e_bases[i] if with_eve else None)
        combos.setdefault(key, []).append(i)
    for (ab, bb, eb), idx in combos.items():
        qc = bb84_circuit(ab, bb, eb)
        mem = sim.run(transpile(qc, sim), shots=len(idx), memory=True,
                      seed_simulator=int(rng.integers(1e6))).result().get_memory()
        for i, m in zip(idx, mem):      # memory string is 'c2 c1 c0'
            a_bits[i] = int(m[-1])
            b_bits[i] = int(m[-2])
    match = a_bases == b_bases
    ka, kb = a_bits[match], b_bits[match]
    # sacrifice half of the sifted key to estimate QBER
    n_test = len(ka) // 2
    qber = np.mean(ka[:n_test] != kb[:n_test])
    final_a, final_b = ka[n_test:], kb[n_test:]
    return {
        "a_bases": a_bases, "b_bases": b_bases, "a_bits": a_bits, "b_bits": b_bits,
        "sifted": int(match.sum()), "n_test": n_test, "qber": qber,
        "final_a": final_a, "final_b": final_b,
        "final_err": np.mean(final_a != final_b),
    }

# ------------------------------------------------------------------
# CHSH test: S = E(a,b) + E(a,b') + E(a',b) - E(a',b')
# Classical (local) limit |S| <= 2, quantum max 2*sqrt(2) ~ 2.828
# ------------------------------------------------------------------
A_ANG = {"a": 0.0, "a'": np.pi / 2}
B_ANG = {"b": np.pi / 4, "b'": -np.pi / 4}

def chsh_E(theta_a, theta_b, with_eve):
    def circ(eve_basis):
        qc = QuantumCircuit(2, 3)
        qc.h(0)
        qc.cx(0, 1)
        if eve_basis is not None:
            rotate_to(qc, 1, eve_basis)
            qc.measure(1, 2)
            rotate_to(qc, 1, eve_basis)
        qc.ry(-theta_a, 0)          # measure along angle theta in X-Z plane
        qc.ry(-theta_b, 1)
        qc.measure(0, 0)
        qc.measure(1, 1)
        return qc
    jobs = [("Z", CHSH_SHOTS // 2), ("X", CHSH_SHOTS // 2)] if with_eve else [(None, CHSH_SHOTS)]
    same = total = 0
    for eb, shots in jobs:
        counts = sim.run(transpile(circ(eb), sim), shots=shots,
                         seed_simulator=int(rng.integers(1e6))).result().get_counts()
        for k, v in counts.items():
            a, b = k[-1], k[-2]
            same += v if a == b else 0
            total += v
    return (2 * same - total) / total

def chsh(with_eve):
    E = {}
    for an, ta in A_ANG.items():
        for bn, tb in B_ANG.items():
            E[(an, bn)] = chsh_E(ta, tb, with_eve)
    S = E[("a", "b")] + E[("a", "b'")] + E[("a'", "b")] - E[("a'", "b'")]
    return E, S

# ------------------------------------------------------------------
log("=" * 70)
log(" TUTORIAL 9 | EXERCISE 4 (REAL-WORLD): Entanglement-based QKD")
log("=" * 70)
log("\nCircuit for one round (Alice=q0, Bob=q1), example: Alice X, Bob X")
log(bb84_circuit("X", "X").draw(output="text"))
log("\nSame round with Eve intercepting Bob's qubit in the Z basis:")
log(bb84_circuit("X", "X", "Z").draw(output="text"))

results = {}
for label, eve in [("No eavesdropper", False), ("With Eve (intercept-resend)", True)]:
    r = run_qkd(eve)
    results[label] = r
    log("\n" + "-" * 70)
    log(f" SCENARIO: {label}")
    log("-" * 70)
    log("First 12 rounds:")
    log(f"  {'#':>3} {'A basis':>8} {'B basis':>8} {'A bit':>6} {'B bit':>6}  kept?")
    for i in range(12):
        kept = "yes" if r["a_bases"][i] == r["b_bases"][i] else "no"
        log(f"  {i:>3} {r['a_bases'][i]:>8} {r['b_bases'][i]:>8} "
            f"{r['a_bits'][i]:>6} {r['b_bits'][i]:>6}  {kept}")
    log(f"\nPairs sent                     : {N_PAIRS}")
    log(f"Rounds with matching bases     : {r['sifted']} "
        f"({100*r['sifted']/N_PAIRS:.1f}%, ~50% expected)")
    log(f"Bits sacrificed for QBER test  : {r['n_test']}")
    log(f"Estimated QBER                 : {100*r['qber']:.2f}%")
    log(f"Final key length               : {len(r['final_a'])} bits")
    log(f"Alice key (first 32)           : {''.join(map(str, r['final_a'][:32]))}")
    log(f"Bob key   (first 32)           : {''.join(map(str, r['final_b'][:32]))}")
    verdict = "SECURE - keep key" if r["qber"] < 0.11 else "ABORT - eavesdropper detected"
    log(f"Decision (QBER threshold 11%)  : {verdict}")

log("\n" + "-" * 70)
log(" CHSH ENTANGLEMENT CHECK  (classical limit |S| <= 2, quantum max 2.828)")
log("-" * 70)
chsh_res = {}
for label, eve in [("No eavesdropper", False), ("With Eve (intercept-resend)", True)]:
    E, S = chsh(eve)
    chsh_res[label] = S
    log(f"\n{label}:")
    for (an, bn), e in E.items():
        log(f"  E({an},{bn}) = {e:+.3f}")
    log(f"  S = {S:.3f}  -> "
        f"{'violates classical bound: genuine entanglement' if abs(S) > 2 else 'within classical bound: entanglement destroyed'}")
log("\n(Note: S comes from finite shots, so it can land slightly above or")
log(" below the ideal 2.828 because of statistical shot noise.)")

log("\n" + "=" * 70)
log(" SUMMARY")
log("=" * 70)
log(f"{'Scenario':<30}{'QBER':>10}{'CHSH S':>10}   Result")
for label in results:
    q = results[label]["qber"]
    s = chsh_res[label]
    ok = q < 0.11 and abs(s) > 2
    log(f"{label:<30}{100*q:>9.2f}%{s:>10.3f}   {'key accepted' if ok else 'key rejected'}")
log("\nHow entanglement secures the channel:")
log("  * Phi+ gives identical results when Alice and Bob use the same basis,")
log("    in Z AND in X, so the matched rounds form a shared random key.")
log("  * The key does not exist until it is measured, so there is nothing")
log("    for Eve to copy in transit, and no-cloning stops her duplicating the qubit.")
log("  * If Eve measures, she breaks the entanglement: errors appear in the")
log("    basis she guessed wrong (~25% QBER) and S drops to the classical range.")
log("  * Alice and Bob detect this publicly and discard the key.")

# ---------- Plots ----------
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
labs = ["No Eve", "With Eve"]
qb = [100 * results[k]["qber"] for k in results]
bars = axes[0].bar(labs, qb, color=["#2a9d8f", "#e76f51"])
axes[0].axhline(11, ls="--", color="black", label="Abort threshold (11%)")
for b, v in zip(bars, qb):
    axes[0].text(b.get_x() + b.get_width() / 2, v + 0.7, f"{v:.1f}%", ha="center")
axes[0].set_ylabel("QBER (%)")
axes[0].set_title("Quantum bit error rate")
axes[0].set_ylim(0, 35)
axes[0].legend()

sv = [chsh_res[k] for k in chsh_res]
bars = axes[1].bar(labs, sv, color=["#2a9d8f", "#e76f51"])
axes[1].axhline(2, ls="--", color="black", label="Classical limit S = 2")
axes[1].axhline(2 * np.sqrt(2), ls=":", color="grey", label="Quantum max 2.828")
for b, v in zip(bars, sv):
    axes[1].text(b.get_x() + b.get_width() / 2, v + 0.05, f"{v:.3f}", ha="center")
axes[1].set_ylabel("CHSH value S")
axes[1].set_title("CHSH entanglement test")
axes[1].set_ylim(0, 3.9)
axes[1].legend(loc="upper right", fontsize=8)
plt.tight_layout()
plt.savefig(os.path.join(OUT, "T09_realworld_qber_chsh.png"), dpi=150)
plt.close()

with open(os.path.join(OUT, "T09_realworld_output.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\nAll outputs saved to: {OUT}")
