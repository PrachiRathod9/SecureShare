# 🛡️ SecureDoc AI: Intelligent Sensitive Data Detection and Document Protection System

**SecureDoc AI** is a production-grade, secure, intelligent sensitive data detection and document protection system built for PDF documents. It enables organizations and individuals to automatically scan documents for confidential credentials and personally identifiable information (PII), assess security risks, apply true coordinate-based text redaction, or enforce whole-document AES-256 password encryption.

---

## 🌟 Key Features

- **🔐 User Authentication**: Secure registration and login with salt + SHA-256/PBKDF2 password hashing.
- **📄 PDF Text Extraction**: High-fidelity page-by-page text extraction powered by PyMuPDF (`fitz`).
- **🔍 Sensitive Data Detection**: Detects Aadhaar numbers, PAN numbers, credit/debit cards, phone numbers, email addresses, passwords, and API keys (AWS, OpenAI `sk-`, Bearer tokens).
- **⚠️ Risk Assessment**: Computes document security risk scores and assigns `HIGH`, `MEDIUM`, or `LOW` risk ratings.
- **🎭 True Redaction & Masking**: Scrubs sensitive content from both the visual rendering and underlying PDF object streams using PyMuPDF coordinate redactions.
- **🔒 AES-256 Encryption**: Password-protects entire PDF files using strong native PDF encryption.
- **🗑️ Temporary File Security**: Ensures zero raw PDF contents or extracted sensitive text strings are saved to the database. Auto-deletes processing temporary files after download or session reset.
- **📊 Activity Logging & Audit Trail**: Keeps track of scan history, risk levels, user actions, and timestamps in MySQL.

---

## 🛠️ Technology Stack

- **Frontend / UI**: Streamlit with custom CSS matching modern cybersecurity aesthetic.
- **Backend / Processing**: Python 3.10+
- **PDF Engine**: PyMuPDF (`fitz`)
- **NLP & Pattern Recognition**: Regex + spaCy (`en_core_web_sm`)
- **Database**: MySQL (PyMySQL connector)
- **Security & Cryptography**: PBKDF2 SHA-256 password hashing, PyCryptodome / Cryptography.

---

## 📂 Project Structure

```
securedoc-ai/
├── app.py              # Main Streamlit router & UI pages
├── auth.py             # User registration & password verification
├── config.py           # Environment variables & constants
├── database.py         # MySQL connection & table initialization
├── detector.py         # Regex & spaCy sensitive data scanner
├── encryptor.py        # PyMuPDF AES-256 PDF encryption
├── logger.py           # Audit trail & file metadata tracking
├── pdf_processor.py    # PyMuPDF text extraction & validation
├── redactor.py         # PyMuPDF coordinate text redaction
├── risk_assessor.py    # Risk scoring & level calculation
├── styles.py           # Custom UI CSS stylesheet
├── temp_manager.py     # Secure temporary file lifecycle manager
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore          # Git exclusion rules
└── README.md           # Project documentation
```

---

## 🔒 Security Best Practices Implemented

1. **No Plain-Text Passwords**: Passwords are hashed using PBKDF2 with unique salts.
2. **Environment Variables**: Sensitive credentials (database passwords, secret keys) are kept in `.env` and excluded from version control.
3. **Data Scrubbing**: Redacted PDFs undergo true structural redaction using PyMuPDF `apply_redactions()`, preventing text recovery via copy/paste or extraction.
4. **Temporary File Deletion**: Temporary files generated during upload and processing are deleted automatically to protect user privacy.
