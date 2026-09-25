import os
import shutil
import uuid
from pathlib import Path
from config import TEMP_DIR

class TempFileManager:
    """Manages temporary storage for PDF uploads and generated files with auto-cleanup."""

    @staticmethod
    def save_uploaded_temp_file(uploaded_file) -> Path:
        """Saves an uploaded Streamlit file to temporary storage with a unique filename."""
        clean_ext = Path(uploaded_file.name).suffix
        temp_filename = f"upload_{uuid.uuid4().hex[:10]}{clean_ext}"
        filepath = TEMP_DIR / temp_filename
        
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        return filepath

    @staticmethod
    def get_output_temp_path(prefix: str = "protected") -> Path:
        """Generates a temporary path for output (redacted or encrypted) PDFs."""
        temp_filename = f"{prefix}_{uuid.uuid4().hex[:10]}.pdf"
        return TEMP_DIR / temp_filename

    @staticmethod
    def cleanup_file(filepath: Path):
        """Safely removes a temporary file if it exists."""
        try:
            if filepath and isinstance(filepath, (str, Path)):
                path_obj = Path(filepath)
                if path_obj.exists() and path_obj.is_file():
                    path_obj.unlink()
        except Exception as e:
            print(f"[Warning] Failed to cleanup temp file {filepath}: {e}")

    @staticmethod
    def cleanup_all_temp_files():
        """Cleans up all files in the temp directory."""
        try:
            for item in TEMP_DIR.glob("*"):
                if item.is_file():
                    try:
                        item.unlink()
                    except Exception:
                        pass
        except Exception as e:
            print(f"[Warning] Temp directory cleanup error: {e}")
