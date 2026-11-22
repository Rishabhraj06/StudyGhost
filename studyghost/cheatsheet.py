"""High-yield 1-page condensed cheatsheet generator."""

import os
import re
from typing import List, Dict


class CheatSheetEngine:
    """Condenses lengthy notes into high-yield 1-page exam revision guides."""

    @classmethod
    def generate(cls, text: str, subject_title: str = "Subject Revision") -> Dict[str, List[str]]:
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        definitions = []
        formulas_or_rules = []
        core_concepts = []

        def_indicators = [
            "is defined as", "refers to", "is a", "is an", "is the process of", 
            "is the", "stands for", "means", "consists of"
        ]
        rule_indicators = ["formula", "theorem", "law", "rule", "protocol", "algorithm", "=", "->", "=>"]

        for line in lines:
            lower = line.lower()
            if any(ind in lower for ind in def_indicators) and len(line) < 220:
                definitions.append(line.lstrip("-•* "))
            elif any(ind in lower for ind in rule_indicators) and len(line) < 200:
                formulas_or_rules.append(line.lstrip("-•* "))
            elif line.startswith(("-", "•", "*", "1.", "2.", "3.")) and len(line) < 180:
                clean = re.sub(r"^[-•*\d.]+\s*", "", line)
                if len(clean) > 20:
                    core_concepts.append(clean)

        # Fallback if text is unstructured prose
        if not definitions and not core_concepts:
            sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 25]
            core_concepts = sentences[:8]

        return {
            "title": subject_title,
            "definitions": definitions[:6],
            "rules_and_formulas": formulas_or_rules[:6],
            "key_takeaways": core_concepts[:8]
        }
