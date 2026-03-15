"""
Master orchestration script for the ParaView AI Visualization Portfolio.

Usage:
    pvpython run_all.py          # Generate data + render all visualizations
    pvpython run_all.py --render # Render only (assumes data already exists)
    pvpython run_all.py --data   # Generate data only
"""
import subprocess
import sys
import os
import time

PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(PROJ_DIR, "scripts")
OUTPUT_DIR = os.path.join(PROJ_DIR, "output")

PVPYTHON = sys.executable

DATA_SCRIPT = os.path.join(SCRIPTS_DIR, "generate_data.py")
VIZ_SCRIPTS = [
    ("Loss Landscape", os.path.join(SCRIPTS_DIR, "viz_loss_landscape.py")),
    ("Gradient Flow Field", os.path.join(SCRIPTS_DIR, "viz_gradient_field.py")),
    ("Activation Volume", os.path.join(SCRIPTS_DIR, "viz_activation_volume.py")),
    ("Embedding Point Cloud", os.path.join(SCRIPTS_DIR, "viz_embedding_cloud.py")),
]


def run_script(label, path):
    print(f"\n{'='*60}")
    print(f"  Running: {label}")
    print(f"  Script:  {path}")
    print(f"{'='*60}")
    start = time.time()
    result = subprocess.run([PVPYTHON, path], cwd=PROJ_DIR)
    elapsed = time.time() - start
    if result.returncode != 0:
        print(f"  [FAILED] {label} (exit code {result.returncode})")
        return False
    print(f"  [OK] {label} completed in {elapsed:.1f}s")
    return True


def main():
    args = sys.argv[1:]
    do_data = "--data" in args or not args
    do_render = "--render" in args or not args

    print("\n" + "#" * 60)
    print("#  ParaView AI Visualization Portfolio - Build Pipeline")
    print("#" * 60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    success = True

    if do_data:
        print("\n>>> Phase 1: Data Generation")
        if not run_script("Data Generation", DATA_SCRIPT):
            print("\nData generation failed. Aborting.")
            sys.exit(1)

    if do_render:
        print("\n>>> Phase 2: Visualization Rendering")
        for label, script_path in VIZ_SCRIPTS:
            if not run_script(label, script_path):
                success = False

    print("\n" + "#" * 60)
    if success:
        print("#  All tasks completed successfully!")
    else:
        print("#  Some tasks failed — check output above.")
    print(f"#  Output directory: {OUTPUT_DIR}")
    print("#" * 60 + "\n")

    generated = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".png")]
    if generated:
        print("Generated images:")
        for f in sorted(generated):
            print(f"  - {f}")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
