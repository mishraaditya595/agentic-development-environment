#!/usr/bin/env python3
"""Entry point for the portable ADE harness without third-party dependencies."""
from pathlib import Path
import sys

here = Path(__file__).resolve()
sys.path.insert(0, str(here.parent if (here.parent / "harness").is_dir() else here.parents[1]))
from harness.core import main

if __name__ == "__main__":
    raise SystemExit(main())
