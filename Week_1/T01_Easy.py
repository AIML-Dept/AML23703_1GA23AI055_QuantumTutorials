
import qiskit
from qiskit_aer import Aer

print("Qiskit version:", qiskit.__version__)
print("Available backends:", [b.name for b in Aer.backends()])