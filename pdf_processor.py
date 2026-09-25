import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Dict, Tuple

class PDFProcessor:
    """Handles text extraction and validation for PDF documents using PyMuPDF."""

    @staticmethod
    def validate_pdf(filepath: Path) -> Tuple[bool, str]:
        """Validates if the file is a readable PDF."""
        if not filepath.exists() or not filepath.is_file():
            return False, "File does not exist."
        
        try:
            doc = fitz.open(filepath)
            if doc.is_encrypted:
                doc.close()
                return False, "Uploaded PDF is password-protected/encrypted. Please upload an unencrypted document."
            
            if len(doc) == 0:
                doc.close()
                return False, "PDF document has no pages."
            
            doc.close()
            return True, "Valid PDF"
        except Exception as e:
            return False, f"Invalid or corrupted PDF file: {str(e)}"

    @staticmethod
    def extract_text(filepath: Path) -> Tuple[List[Dict], int, str]:
        """
        Extracts text page-by-page.
        Returns:
            - List of page dicts: [{'page_num': 1, 'text': '...'}]
            - Total page count
            - Full extracted text string
        """
        doc = fitz.open(filepath)
        pages_data = []
        full_text_list = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text") or ""
            pages_data.append({
                "page_num": page_num + 1,
                "text": text
            })
            full_text_list.append(text)

        total_pages = len(doc)
        doc.close()
        full_text = "\n".join(full_text_list)

        return pages_data, total_pages, full_text
