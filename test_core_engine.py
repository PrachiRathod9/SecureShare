import fitz
from temp_manager import TempFileManager
from pdf_processor import PDFProcessor
from detector import SensitiveDataDetector
from risk_assessor import RiskAssessor
from redactor import PDFRedactor
from encryptor import PDFEncryptor

def test_core():
    print("--- 1. Testing Core PDF & Sensitive Data Processing ---")
    test_pdf_path = TempFileManager.get_output_temp_path("pure_mysql_test_input")
    doc = fitz.open()
    page = doc.new_page()
    sample_text = (
        "CONFIDENTIAL DOCUMENT\n"
        "Employee: Rajesh Kumar\n"
        "Aadhaar Number: 4589 1234 5678\n"
        "PAN Card: ABCDE1234F\n"
        "Contact Email: rajesh.k@example.com\n"
        "Phone: +91 9876543210\n"
        "System Password: MySuperSecret123\n"
        "API Key: sk-proj-abcdef1234567890abcdef123456\n"
    )
    page.insert_text((50, 50), sample_text, fontsize=12)
    doc.save(test_pdf_path)
    doc.close()

    # Validate & extract
    valid, msg = PDFProcessor.validate_pdf(test_pdf_path)
    assert valid == True, f"PDF validation failed: {msg}"
    pages_data, total_pages, full_text = PDFProcessor.extract_text(test_pdf_path)

    # Detect
    detections, summary_counts, total_count = SensitiveDataDetector.scan_pages(pages_data)
    assert total_count > 0, "No sensitive data detected!"

    # Risk Assessment
    risk_level, score, desc = RiskAssessor.evaluate_risk(summary_counts, total_count)
    assert risk_level in ["HIGH", "MEDIUM"], "Risk level evaluation failed!"

    # Redaction
    redacted_pdf_path = TempFileManager.get_output_temp_path("pure_mysql_test_redacted")
    redact_ok = PDFRedactor.redact_pdf(test_pdf_path, redacted_pdf_path, detections)
    assert redact_ok == True, "Redaction failed!"

    # Encryption
    encrypted_pdf_path = TempFileManager.get_output_temp_path("pure_mysql_test_encrypted")
    encrypt_ok = PDFEncryptor.encrypt_pdf(test_pdf_path, encrypted_pdf_path, "SecurePass2026")
    assert encrypt_ok == True, "Encryption failed!"

    # Cleanup
    TempFileManager.cleanup_file(test_pdf_path)
    TempFileManager.cleanup_file(redacted_pdf_path)
    TempFileManager.cleanup_file(encrypted_pdf_path)

    print("[SUCCESS] Core PDF processing, detection, redaction, and encryption engines are 100% operational!")

if __name__ == "__main__":
    test_core()
