import fitz  # PyMuPDF
import re
from pathlib import Path
from typing import List, Dict

class PDFRedactor:
    """Applies true coordinate-based text redaction to PDF documents using PyMuPDF."""

    @staticmethod
    def redact_pdf(input_path: Path, output_path: Path, detections: List[Dict]) -> bool:
        """
        Redacts detected sensitive strings from the PDF.
        Overwrites text with black rectangle annotations and applies redactions to completely scrub content.
        """
        try:
            doc = fitz.open(input_path)

            # Group raw sensitive values by page number
            page_detections: Dict[int, set] = {}
            for item in detections:
                p_num = item["page_num"] - 1  # 0-indexed page in fitz
                raw_val = item["raw_value"].strip()
                if raw_val:
                    if p_num not in page_detections:
                        page_detections[p_num] = set()
                    page_detections[p_num].add(raw_val)
                    
                    # If raw_val contains key-value pair like 'password = secret', also add 'secret'
                    if ":" in raw_val or "=" in raw_val:
                        parts = re.split(r"[:=]", raw_val, maxsplit=1)
                        if len(parts) == 2 and parts[1].strip():
                            page_detections[p_num].add(parts[1].strip())

            for page_index in range(len(doc)):
                page = doc[page_index]
                if page_index in page_detections:
                    for text_to_redact in page_detections[page_index]:
                        # Search for matching text bounding boxes
                        rects = page.search_for(text_to_redact)
                        for rect in rects:
                            # Add redaction annotation (fill with black background)
                            page.add_redact_annot(rect, fill=(0, 0, 0))

                    # Apply redactions to permanently scrub text from PDF structure
                    page.apply_redactions()

            # Save the clean PDF file
            doc.save(output_path, garbage=4, deflate=True)
            doc.close()
            return True
        except Exception as e:
            print(f"[Error] PDF redaction failed: {e}")
            return False
