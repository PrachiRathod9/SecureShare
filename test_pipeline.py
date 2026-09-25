import fitz  # PyMuPDF
from pathlib import Path
from temp_manager import TempFileManager
from pdf_processor import PDFProcessor
from detector import SensitiveDataDetector
from risk_assessor import RiskAssessor
from redactor import PDFRedactor
from encryptor import PDFEncryptor
from auth import register_user, login_user

def run_tests():
    print("--- 1. Testing Auth Module ---")
    reg_ok, user_data = register_user("Test User", "test@securedoc.ai", "SecretPass123!")
    print(f"Register result: {reg_ok}, user: {user_data}")
    
    login_ok, login_data = login_user("test@securedoc.ai", "SecretPass123!")
    print(f"Login result: {login_ok}, user: {login_data}")
    assert login_ok == True, "Auth login failed!"

    print("\n--- 2. Creating Sample Test PDF ---")
    test_pdf_path = TempFileManager.get_output_temp_path("test_input")
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
    print(f"Created test PDF at: {test_pdf_path}")

    print("\n--- 3. Testing PDF Processor & Detector ---")
    valid, msg = PDFProcessor.validate_pdf(test_pdf_path)
    assert valid == True, f"PDF validation failed: {msg}"
    
    pages_data, total_pages, full_text = PDFProcessor.extract_text(test_pdf_path)
    print(f"Extracted {total_pages} page(s), length: {len(full_text)} chars")

    detections, summary_counts, total_count = SensitiveDataDetector.scan_pages(pages_data)
    print(f"Total Detections: {total_count}")
    print(f"Summary Counts: {summary_counts}")
    for d in detections:
        print(f"  - [{d['type']}] Masked: {d['masked_value']} (Page {d['page_num']})")

    assert total_count > 0, "Detector failed to find sensitive data!"

    print("\n--- 4. Testing Risk Assessor ---")
    risk_level, score, desc = RiskAssessor.evaluate_risk(summary_counts, total_count)
    print(f"Risk Level: {risk_level}, Score: {score}")
    print(f"Description: {desc}")
    assert risk_level in ["HIGH", "MEDIUM"], "Risk assessment level mismatch!"

    print("\n--- 5. Testing Redaction Engine ---")
    redacted_pdf_path = TempFileManager.get_output_temp_path("test_redacted")
    redact_ok = PDFRedactor.redact_pdf(test_pdf_path, redacted_pdf_path, detections)
    print(f"Redaction result: {redact_ok}, Output PDF: {redacted_pdf_path}")
    assert redact_ok == True, "Redaction failed!"

    # Verify redacted PDF text does not contain original sensitive password/Aadhaar
    red_pages, _, red_full_text = PDFProcessor.extract_text(redacted_pdf_path)
    print(f"Redacted PDF text preview (length {len(red_full_text)} chars):")
    print(red_full_text.strip())
    assert "4589 1234 5678" not in red_full_text, "Aadhaar was not redacted!"
    assert "MySuperSecret123" not in red_full_text, "Password was not redacted!"

    print("\n--- 6. Testing Encryption Engine ---")
    encrypted_pdf_path = TempFileManager.get_output_temp_path("test_encrypted")
    encrypt_ok = PDFEncryptor.encrypt_pdf(test_pdf_path, encrypted_pdf_path, "SecurePass2026")
    print(f"Encryption result: {encrypt_ok}, Output PDF: {encrypted_pdf_path}")
    assert encrypt_ok == True, "Encryption failed!"

    # Verify encrypted PDF cannot be opened without password
    enc_valid, enc_msg = PDFProcessor.validate_pdf(encrypted_pdf_path)
    print(f"Encrypted PDF validation (should fail password check): {enc_valid}, msg: {enc_msg}")
    assert enc_valid == False, "Encrypted PDF opened without password!"

    print("\n--- 7. Cleaning up Temporary Files ---")
    TempFileManager.cleanup_file(test_pdf_path)
    TempFileManager.cleanup_file(redacted_pdf_path)
    TempFileManager.cleanup_file(encrypted_pdf_path)
    print("Cleaned up temp files successfully.")

    print("\n[SUCCESS] ALL SYSTEM TESTS PASSED PERFECTLY!")

if __name__ == "__main__":
    run_tests()
