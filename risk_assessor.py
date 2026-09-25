from typing import Dict, Tuple
from config import RISK_WEIGHTS, RISK_LEVELS

class RiskAssessor:
    """Evaluates risk score and assigns LOW / MEDIUM / HIGH risk ratings."""

    @staticmethod
    def evaluate_risk(summary_counts: Dict[str, int], total_count: int) -> Tuple[str, int, str]:
        """
        Calculates total risk score based on detection category weights.
        Returns:
            - Risk Level: 'HIGH', 'MEDIUM', or 'LOW'
            - Numerical Risk Score
            - Risk description text
        """
        if total_count == 0:
            return "LOW", 0, "No sensitive information detected in document."

        score = 0
        for category, count in summary_counts.items():
            weight = RISK_WEIGHTS.get(category, 5)
            score += weight * count

        # Determine level based on thresholds
        if score >= RISK_LEVELS["HIGH"] or summary_counts.get("Password", 0) > 0 or summary_counts.get("API Key", 0) > 0:
            level = "HIGH"
            desc = "Critical sensitive credentials or confidential identifiers detected. Immediate redaction or encryption recommended."
        elif score >= RISK_LEVELS["MEDIUM"] or summary_counts.get("Aadhaar", 0) > 0 or summary_counts.get("PAN", 0) > 0 or summary_counts.get("Credit Card", 0) > 0:
            level = "MEDIUM"
            desc = "Personally Identifiable Information (PII) detected. Document requires protection before sharing."
        else:
            level = "LOW"
            desc = "Low-risk contact details detected. Review and redact if required."

        return level, score, desc
