"""
Standalone data generation script (no ParaView dependency).
Uses only NumPy. Run this with standard Python if pvpython is unavailable.

Usage:
    python scripts/generate_data_standalone.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from generate_data import (
    generate_loss_landscape,
    generate_gradient_field,
    generate_activation_volume,
    generate_embedding_cloud,
)

if __name__ == "__main__":
    print("=" * 60)
    print("  Generating datasets (standalone mode)")
    print("=" * 60)
    generate_loss_landscape()
    generate_gradient_field()
    generate_activation_volume()
    generate_embedding_cloud()
    print("\nDone. Data files are in the 'data/' directory.")
