import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

print("Real-World: Phase Kickback Applied to a Binary Classification Decision\n")

explanation = """
Conceptual mapping: Deutsch's phase kickback -> binary classification

1. INPUT ENCODING
   A data point's feature is encoded into the input qubit's superposition
   state (analogous to |x> = alpha|0> + beta|1>).

2. ORACLE = CLASSIFIER FUNCTION
   The oracle Uf represents a trained decision function f(x) that outputs
   a binary class label (0 or 1) for each possible input state.

3. PHASE KICKBACK
   Because the ancilla qubit is prepared in the |-> state before the oracle
   acts, the classifier's output f(x) is not written to a separate output
   register - it is 'kicked back' as a phase (-1)^f(x) onto the input
   qubit's own amplitude, without collapsing the superposition.

4. INTERFERENCE = DECISION READOUT
   A final Hadamard gate on the input qubit converts this phase difference
   into a measurable amplitude difference. Measuring the qubit then reveals
   the classification outcome (constant-like vs balanced-like decision
   boundary) in a single query, instead of needing to evaluate f explicitly
   for every possible input as a classical classifier would.
"""
print(explanation)

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.set_xlim(0, 10.5)
ax.set_ylim(0, 4)
ax.axis("off")

boxes = [
    ("Input Feature\n(qubit superposition)", 0.3, 1.3, 2.0, 1.4),
    ("Oracle Uf\n(classifier function)", 2.9, 1.3, 2.0, 1.4),
    ("Phase Kickback\n(-1)^f(x) on input", 5.5, 1.3, 2.0, 1.4),
    ("Hadamard + Measure\n(decision readout)", 8.1, 1.3, 1.9, 1.4),
]

for label, x, y, w, h in boxes:
    rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                                    linewidth=1.5, edgecolor="#1f77b4", facecolor="#e8f1fb")
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=9.5)

arrow_props = dict(arrowstyle="->", linewidth=1.5, color="#333333")
ax.annotate("", xy=(2.9, 2.0), xytext=(2.3, 2.0), arrowprops=arrow_props)
ax.annotate("", xy=(5.5, 2.0), xytext=(4.9, 2.0), arrowprops=arrow_props)
ax.annotate("", xy=(8.1, 2.0), xytext=(7.5, 2.0), arrowprops=arrow_props)

ax.set_title("Phase Kickback Applied to a Binary Classification Decision", fontsize=12, pad=15)

os.makedirs("output", exist_ok=True)
plt.savefig("output/T07_realworld_output.png", bbox_inches="tight", dpi=150)
print("Diagram saved to output/T07_realworld_output.png")

with open("output/T07_realworld_output.txt", "w") as f:
    f.write(explanation)

print("Explanation saved to output/T07_realworld_output.txt")
