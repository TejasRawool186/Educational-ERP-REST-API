"""
seed_all.py
-----------
Convenience runner that executes all seed scripts in order.

Usage:
    python scripts/seed_all.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from scripts import (
    _01_create_schema as s01,
    _02_seed_master as s02,
    _03_seed_faculty as s03,
    _04_seed_courses as s04,
    _05_seed_students as s05,
    _06_seed_academics as s06,
    _07_seed_career as s07,
    _08_validate_dataset as s08,
)

# expose importable names for the convenience runner
import importlib, pathlib

def run_step(module_path):
    name = pathlib.Path(module_path).stem
    print(f"\n{'='*60}")
    print(f"  Running: {name}")
    print('='*60)
    spec = importlib.util.spec_from_file_location(name, module_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if hasattr(mod, "main"):
        mod.main()
    elif hasattr(mod, "seed"):
        mod.seed()
    elif hasattr(mod, "run"):
        mod.run()


if __name__ == "__main__":
    scripts_dir = os.path.dirname(__file__)
    steps = sorted(
        p for p in (os.path.join(scripts_dir, f) for f in os.listdir(scripts_dir))
        if p.endswith(".py") and os.path.basename(p)[0].isdigit()
    )
    for step in steps:
        run_step(step)
    print("\nAll seed steps complete.")
