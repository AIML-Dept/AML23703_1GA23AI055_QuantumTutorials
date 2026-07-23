"""
Tutorial No. : T01 | Date: 23-07-2026 | Level: Easy
Objective    : Install Qiskit and verify installation.
USN          : 1GA23AI055
"""

import qiskit
from qiskit_aer import Aer

print("Qiskit version:", qiskit.__version__)
print("Available backends:", [b.name for b in Aer.backends()])