import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

n_values = list(range(2, 11))
simon_queries = [n for n in n_values]
classical_queries = [2 ** (n / 2) for n in n_values]

print(f"{'n':^5}{'Simon (queries)':^20}{'Classical (expected)':^25}")
print("-" * 50)
for n, sq, cq in zip(n_values, simon_queries, classical_queries):
    print(f"{n:^5}{sq:^20}{cq:^25.1f}")

plt.figure(figsize=(8, 5))
plt.plot(n_values, simon_queries, marker='o', label="Simon's algorithm (quantum)")
plt.plot(n_values, classical_queries, marker='s', label="Classical brute-force (expected)")
plt.yscale('log')
plt.xlabel("Secret string length n (bits)")
plt.ylabel("Number of oracle queries (log scale)")
plt.title("Simon's Algorithm vs Classical Brute-Force: Query Complexity")
plt.legend()
plt.grid(True, which="both", linestyle="--", alpha=0.5)

os.makedirs("output", exist_ok=True)
plt.savefig("output/T06_realworld_output.png", bbox_inches="tight")
print("\nPlot saved to output/T06_realworld_output.png")

with open("output/T06_realworld_output.txt", "w") as f:
    f.write(f"{'n':^5}{'Simon':^15}{'Classical':^20}\n")
    for n, sq, cq in zip(n_values, simon_queries, classical_queries):
        f.write(f"{n:^5}{sq:^15}{cq:^20.1f}\n")
print("Summary saved to output/T06_realworld_output.txt")
