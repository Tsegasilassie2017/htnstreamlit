"""Backward-compatible entry point (Streamlit Cloud can keep pointing here)."""
import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).parent / "app" / "streamlit_app.py"), run_name="__main__")
