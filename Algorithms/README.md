# Quantum Algorithms with PennyLane

This repository contains simple implementations of quantum algorithms using the PennyLane framework. It is intended as a learning and experimentation space for exploring Grover-style search circuits, oracle construction, and quantum circuit design in Python.

## Overview

The project demonstrates basic quantum computing concepts such as:

- Grover's algorithm components
- Oracle construction for marked states
- Phase-flip oracles
- Quantum circuit execution using PennyLane's simulator

## Repository Contents

- `grovers.py` - A basic Grover-style circuit implementation
- `non_pair_oracle.py` - An oracle example without pairing logic
- `oracle_matrix.py` - Utility for generating oracle matrices
- `oracle_pair.py` - An oracle example involving paired-state logic

## Requirements

Make sure you have Python 3.10+ installed.

Install the required dependencies:

```bash
pip install pennylane numpy
```

If you want to use the virtual environment already included in this workspace:

```bash
source myenv/bin/activate
```

## Running the Examples

Run the scripts directly with Python:

```bash
python grovers.py
python non_pair_oracle.py
python oracle_matrix.py
python oracle_pair.py
```

## Project Structure

```text
.
├── grovers.py
├── non_pair_oracle.py
├── oracle_matrix.py
├── oracle_pair.py
└── myenv/                  # Local Python virtual environment
```

## Notes

These scripts are educational examples and are meant to help understand how quantum oracles and amplitude amplification work in PennyLane.

## Future Goals

Possible extensions for this repository include:

- Adding more quantum algorithms such as QFT or Shor-inspired examples
- Improving modularity and reusable circuit components
- Adding comments and visualization for circuit execution
- Including unit tests and example notebooks

## Contributing

Feel free to improve the examples, add new algorithms, or refactor the code for clarity.
