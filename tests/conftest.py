"""Import pure helpers without loading the Sublime plugin."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
