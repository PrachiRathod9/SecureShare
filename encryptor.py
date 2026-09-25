import fitz  # PyMuPDF
import secrets
from pathlib import Path

class PDFEncryptor:
    """Applies strong AES-256 encryption to entire PDF documents."""

    @staticmethod
    def encrypt_pdf(input_path: Path, output_path: Path, password: str) -> bool:
        """
        Encrypts the PDF using PyMuPDF AES-256 encryption requiring a password to open.
        """
        try:
            if not password or len(password.strip()) == 0:
                return False

            doc = fitz.open(input_path)
            
            # Generate a random owner password for administrative rights
            owner_pw = secrets.token_hex(16)

            # Save with AES-256 encryption
            doc.save(
                output_path,
                encryption=fitz.PDF_ENCRYPT_AES_256,
                user_pw=password,
                owner_pw=owner_pw,
                permissions=fitz.PDF_PERM_ACCESSIBILITY
            )
            doc.close()
            return True
        except Exception as e:
            print(f"[Error] PDF encryption failed: {e}")
            return False
