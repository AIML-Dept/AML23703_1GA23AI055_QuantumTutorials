import matplotlib
matplotlib.use("Agg")
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import os

def simon_oracle(b):
    b = b[::-1]
    n = len(b)
    qc = QuantumCircuit(n * 2)
    for q in range(n):
        qc.cx(q, q + n)
    if '1' not in b:
        return qc
    i = b.find('1')
    for q in range(n):
        if b[q] == '1':
            qc.cx(i, q + n)
    return qc

def gf2_solve(equations, n):
    rows = [list(map(int, eq)) for eq in equations if eq != '0' * n]
    m = len(rows)
    pivot_cols = []
    r = 0
    for c in range(n):
        pivot = None
        for i in range(r, m):
            if rows[i][c] == 1:
                pivot = i
                break
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        for i in range(m):
            if i != r and rows[i][c] == 1:
                rows[i] = [a ^ b for a, b in zip(rows[i], rows[r])]
        pivot_cols.append(c)
        r += 1
        if r == m:
            break
    free_cols = [c for c in range(n) if c not in pivot_cols]
    if not free_cols:
        return None
    free_col = free_cols[0]
    s = [0] * n
    s[free_col] = 1
    for i, pc in enumerate(pivot_cols):
        s[pc] = rows[i][free_col]
    return ''.join(map(str, s))

n = 3
s = '110'
sim = AerSimulator()

qc = QuantumCircuit(2 * n, n)
qc.h(range(n))
qc.barrier()
qc.compose(simon_oracle(s), inplace=True)
qc.barrier()
qc.h(range(n))
qc.measure(range(n), range(n))

print(qc.draw())

result = sim.run(qc, shots=1024).result()
counts = result.get_counts()
print("\nMeasurement counts:", counts)

equations = list(counts.keys())
print(f"\nCollected {len(equations)} distinct measurement outcomes (equations):")
for eq in equations:
    print(f"  {eq} . s = 0 (mod 2)")

recovered_s = gf2_solve(equations, n)
print(f"\nSecret string recovered: {recovered_s}")
print(f"Actual secret string:    {s}")
print(f"Match: {recovered_s == s}")

os.makedirs("output", exist_ok=True)
fig = plot_histogram(counts)
fig.savefig("output/T06_medium_output.png", bbox_inches="tight")
print("\nHistogram saved to output/T06_medium_output.png")

with open("output/T06_medium_output.txt", "w") as f:
    f.write(f"Secret string: {s}\n")
    f.write(f"Measurement counts: {counts}\n")
    f.write(f"Equations collected: {equations}\n")
    f.write(f"Recovered secret: {recovered_s}\n")
    f.write(f"Match: {recovered_s == s}\n")
print("Summary saved to output/T06_medium_output.txt")
