"""
Streamlit Community Cloud root entry point.
Launches the frontend application located at frontend/streamlit_app.py.
"""
from pathlib import Path
import runpy

frontend_path = Path(__file__).resolve().parent / "frontend" / "streamlit_app.py"
runpy.run_path(str(frontend_path), run_name="__main__")
