"""
AegisPay-AI: Semantic Guardrail & Payload Inspector (Pillar 3 - DEFEND Level 4)
Inspects text memos, agentic checkout instructions, and ISO 20022 XML payloads
for prompt injection, malicious CDATA, and social engineering cues (<15ms).
"""
import re
from typing import Dict, Any, List, Optional

from red_team.generator import TransactionRecord


class SemanticGuardrailDetector:
    """
    NLP and pattern-matching guardrail protecting against GenAI-driven payload attacks.
    """

    PROMPT_INJECTION_PATTERNS = [
        r"<\|system\|>",
        r"<\|im_start\|>",
        r"\[INST\]",
        r"SYSTEM OVERRIDE",
        r"disregard prior",
        r"ignore previous instructions",
        r"route .* to (?:vpa|iban|address)",
        r"escrow guarantee.*transfer",
        r"transfer.*to.*mule",
    ]

    MALICIOUS_XML_PATTERNS = [
        r"<!\[CDATA\[.*ADMIN.*\]\]>",
        r"&xxe_",
        r"SET status\s*=\s*'SETTLED'",
        r"DROP\s+LOGS",
        r"RECON_BYPASS_FLAG",
    ]

    SOCIAL_ENGINEERING_CUES = [
        r"emergency.*family",
        r"hospital.*urgent",
        r"compromised account.*transfer immediately",
        r"police.*bail.*wire",
    ]

    def __init__(self):
        self.injection_regex = [re.compile(p, re.IGNORECASE) for p in self.PROMPT_INJECTION_PATTERNS]
        self.xml_regex = [re.compile(p, re.IGNORECASE) for p in self.MALICIOUS_XML_PATTERNS]
        self.se_regex = [re.compile(p, re.IGNORECASE) for p in self.SOCIAL_ENGINEERING_CUES]

    def inspect_payload(self, tx: TransactionRecord) -> Dict[str, Any]:
        """
        Scans transaction remittance memo, agent instruction trace, and XML IDs.
        """
        text_corpus = f"{tx.remittance_memo or ''} {tx.agent_instruction_trace or ''}"

        # 1. Check for LLM Prompt Injections in Agentic Commerce
        prompt_injection_hits = []
        for r in self.injection_regex:
            m = r.search(text_corpus)
            if m:
                prompt_injection_hits.append(m.group(0))

        # 2. Check for Malicious ISO 20022 XML Injections
        xml_hits = []
        for r in self.xml_regex:
            m = r.search(text_corpus)
            if m:
                xml_hits.append(m.group(0))

        # 3. Check for Conversational APP Social Engineering Cues
        se_hits = []
        for r in self.se_regex:
            m = r.search(text_corpus)
            if m:
                se_hits.append(m.group(0))

        # Calculate semantic risk score
        risk_score = 0.01

        if prompt_injection_hits:
            risk_score = max(risk_score, 0.98)
        if xml_hits:
            risk_score = max(risk_score, 0.96)
        if se_hits and tx.amount > 2500.0:
            risk_score = max(risk_score, 0.88)

        is_flagged = (len(prompt_injection_hits) > 0 or len(xml_hits) > 0 or len(se_hits) > 0)

        return {
            "semantic_risk_score": round(float(risk_score), 4),
            "payload_compromised": is_flagged,
            "detected_injection_tokens": prompt_injection_hits,
            "detected_xml_exploits": xml_hits,
            "social_engineering_markers": se_hits,
            "guardrail_verdict": "FLAGGED_MALICIOUS_PAYLOAD" if is_flagged else "CLEAN_PAYLOAD"
        }
