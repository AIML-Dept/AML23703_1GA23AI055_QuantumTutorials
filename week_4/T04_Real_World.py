from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

# Qubits: q0=A, q1=B, q2=Cin, q3=Sum, q4=Cout
# We test A=1, B=1, Cin=1 -> Sum=1, Cout=1

qc = QuantumCircuit(5, 2)

# Set inputs
qc.x(0)   # A = 1
qc.x(1)   # B = 1
qc.x(2)   # Cin = 1

qc.barrier()

# Compute Sum = A XOR B XOR Cin  -> store in q3
qc.cx(0, 3)
qc.cx(1, 3)
qc.cx(2, 3)

# Compute Cout = majority(A, B, Cin) -> store in q4
qc.ccx(0, 1, 4)   # A AND B
qc.ccx(1, 2, 4)   # B AND Cin  (accumulates OR since q4 starts at 0)
qc.ccx(0, 2, 4)   # A AND Cin

qc.barrier()
qc.measure(3, 0)  # Sum
qc.measure(4, 1)  # Cout

print(qc.draw())

sim = AerSimulator()
result = sim.run(qc, shots=1024).result()
counts = result.get_counts()
print("Counts (bit order: Cout Sum):", counts)   # Expect '11' i.e. Sum=1, Cout=1
plot_histogram(counts)