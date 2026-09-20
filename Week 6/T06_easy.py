from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
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

n = 3
s = '110'
sim = AerSimulator()

print(f"Simon oracle truth table for secret string s = {s}\n")
print(f"{'x':^8}{'f(x)':^8}")
print("-" * 18)

table = {}
for x_int in range(2 ** n):
    x = format(x_int, f'0{n}b')
    qc = QuantumCircuit(2 * n, n)
    for i, bit in enumerate(reversed(x)):
        if bit == '1':
            qc.x(i)
    qc.compose(simon_oracle(s), inplace=True)
    qc.measure(range(n, 2 * n), range(n))
    result = sim.run(qc, shots=1).result()
    counts = result.get_counts()
    fx = list(counts.keys())[0]
    table[x] = fx
    print(f"{x:^8}{fx:^8}")

print("\nVerification: f(x) should equal f(x XOR s) for every x\n")
all_ok = True
for x, fx in table.items():
    x_xor_s = format(int(x, 2) ^ int(s, 2), f'0{n}b')
    fx_xor = table[x_xor_s]
    match = "OK" if fx == fx_xor else "MISMATCH"
    if fx != fx_xor:
        all_ok = False
    print(f"f({x}) = {fx}   f({x_xor_s}) = {fx_xor}   -> {match}")

print(f"\nOracle correctness verified: {all_ok}")

os.makedirs("output", exist_ok=True)
with open("output/T06_easy_output.txt", "w") as f:
    f.write(f"Simon oracle truth table for secret string s = {s}\n\n")
    f.write(f"{'x':^8}{'f(x)':^8}\n")
    f.write("-" * 18 + "\n")
    for x, fx in table.items():
        f.write(f"{x:^8}{fx:^8}\n")
    f.write(f"\nOracle correctness verified: {all_ok}\n")

print("\nOutput saved to output/T06_easy_output.txt")
