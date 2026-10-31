#!/usr/bin/env python3
"""Run the tools from this exact checkout without installing the project."""

from pathlib import Path
import sys


CHECKOUT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CHECKOUT / "src"))

from labo_tools.cli import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main(checkout=CHECKOUT))
