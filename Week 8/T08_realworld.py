import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

n_values = list(range(2, 11))
classical_worst_case = [2 ** (n - 1) + 1 for n in n_values]
quantum_queries = [1 for _ in n_values]

print(f"{'n':^5}{'Classical (worst-case)':^25}{'Quantum':^10}")
print("-" * 40)
for n, cq, qq in zip(n_values, classical_worst_case, quantum_queries):
    print(f"{n:^5}{cq:^25}{qq:^10}")

plt.figure(figsize=(8, 5))
plt.plot(n_values, classical_worst_case, marker='s', label="Classical (worst-case, 2^(n-1)+1)")
plt.plot(n_values, quantum_queries, marker='o', label="Quantum (Deutsch-Jozsa, always 1)")
plt.yscale('log')
plt.xlabel("Number of input bits n")
plt.ylabel("Number of oracle queries (log scale)")
plt.title("Deutsch-Jozsa Algorithm: Classical vs Quantum Query Complexity")
plt.legend()
plt.grid(True, which="both", linestyle="--", alpha=0.5)

os.makedirs("output", exist_ok=True)
plt.savefig("output/T08_realworld_output.png", bbox_inches="tight", dpi=150)
print("\nPlot saved to output/T08_realworld_output.png")

with open("output/T08_realworld_output.txt", "w") as f:
    f.write(f"{'n':^5}{'Classical (worst-case)':^25}{'Quantum':^10}\n")
    for n, cq, qq in zip(n_values, classical_worst_case, quantum_queries):
        f.write(f"{n:^5}{cq:^25}{qq:^10}\n")
print("Summary saved to output/T08_realworld_output.txt")
