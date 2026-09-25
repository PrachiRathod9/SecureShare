import re
from typing import List, Dict, Tuple

# Try loading spacy model, fallback if not downloaded
SPACY_AVAILABLE = False
try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
        SPACY_AVAILABLE = True
    except Exception:
        SPACY_AVAILABLE = False
except ImportError:
    SPACY_AVAILABLE = False

class SensitiveDataDetector:
    """Detects sensitive personal and security credentials in document text."""

    PATTERNS = {
        "Aadhaar": r"\b[2-9]{1}[0-9]{3}[\s\-]?[0-9]{4}[\s\-]?[0-9]{4}\b",
        "PAN": r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b",
        "Credit Card": r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12}|[0-9]{4}[\s\-][0-9]{4}[\s\-][0-9]{4}[\s\-][0-9]{4})\b",
        "Password": r"(?i)\b(?:password|passwd|pwd|passphrase|secret_key|app_secret)[\s:=]+(\S+)",
        "API Key": r"\b(?:sk-[a-zA-Z0-9\-_]{20,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z\-_]{35}|ghp_[a-zA-Z0-9]{36}|bearer\s+[a-zA-Z0-9\-\._~\+\/]+=*)\b",
        "Phone Number": r"\b(?:\+91[\-\s]?)?[6-9]\d{9}\b",
        "Email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    }

    @staticmethod
    def mask_value(category: str, raw_val: str) -> str:
        """Returns a sanitized/masked representation of sensitive strings."""
        val = raw_val.strip()
        if category == "Aadhaar":
            clean = re.sub(r"\D", "", val)
            if len(clean) == 12:
                return f"XXXX XXXX {clean[-4:]}"
            return "XXXX XXXX 1234"
        elif category == "PAN":
            if len(val) == 10:
                return f"XXXXX{val[5:]}"
            return "ABCDE1234F"
        elif category == "Password":
            return "********"
        elif category == "API Key":
            if val.startswith("sk-"):
                return "sk-********************"
            return "key-********************"
        elif category == "Credit Card":
            clean = re.sub(r"\D", "", val)
            if len(clean) >= 4:
                return f"XXXX-XXXX-XXXX-{clean[-4:]}"
            return "XXXX-XXXX-XXXX-1234"
        elif category == "Phone Number":
            clean = re.sub(r"\D", "", val)
            if len(clean) >= 10:
                return f"+91 XXXXX-{clean[-4:]}"
            return "XXXXXX1234"
        elif category == "Email":
            parts = val.split("@")
            if len(parts) == 2:
                name, domain = parts
                masked_name = name[0] + "***" + name[-1] if len(name) > 2 else "***"
                return f"{masked_name}@{domain}"
            return "u***r@domain.com"
        return "********"

    @classmethod
    def scan_pages(cls, pages_data: List[Dict]) -> Tuple[List[Dict], Dict[str, int], int]:
        """
        Scans page text for sensitive data matches.
        Returns:
            - List of detailed detection records: [{'type': 'Aadhaar', 'raw_value': '...', 'masked_value': '...', 'page_num': 1}]
            - Summary count per category: {'Aadhaar': 3, 'PAN': 2, ...}
            - Total detection count
        """
        detections = []
        summary_counts = {cat: 0 for cat in cls.PATTERNS.keys()}

        for page in pages_data:
            page_num = page["page_num"]
            text = page["text"]

            for category, pattern in cls.PATTERNS.items():
                matches = re.finditer(pattern, text)
                for match in matches:
                    raw_val = match.group(0)

                    # Ignore trivial false positives for phone numbers/numbers
                    if category == "Phone Number" and len(re.sub(r"\D", "", raw_val)) != 10:
                        continue

                    masked_val = cls.mask_value(category, raw_val)

                    detections.append({
                        "type": category,
                        "raw_value": raw_val,
                        "masked_value": masked_val,
                        "page_num": page_num
                    })

                    summary_counts[category] = summary_counts.get(category, 0) + 1

        total_count = len(detections)
        return detections, summary_counts, total_count
