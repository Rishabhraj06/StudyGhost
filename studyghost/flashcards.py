"""Anki & spaced-repetition flashcard generator."""

import csv
import io
import re
from dataclasses import dataclass
from typing import List


@dataclass
class Flashcard:
    front: str
    back: str
    tag: str = "studyghost"


class FlashcardEngine:
    """Creates Anki and spaced-repetition flashcards from study notes."""

    @classmethod
    def generate(cls, text: str, max_cards: int = 10) -> List[Flashcard]:
        cards: List[Flashcard] = []
        lines = [l.strip() for l in text.splitlines() if l.strip()]

        # Pattern 1: Concept: Definition or Term - Definition
        pattern_split = re.compile(r"^([^:–—\-]+)[:–—\-]\s*(.+)$")

        for line in lines:
            m = pattern_split.match(line)
            if m:
                term, definition = m.groups()
                term = term.strip().lstrip("•*- 1234567890.")
                definition = definition.strip()
                if 2 < len(term) < 40 and len(definition) > 15:
                    cards.append(Flashcard(
                        front=f"What is {term}?",
                        back=definition,
                        tag="exam-core"
                    ))
            elif "is defined as" in line.lower() or "refers to" in line.lower():
                parts = re.split(r"is defined as|refers to", line, flags=re.IGNORECASE)
                if len(parts) == 2:
                    term = parts[0].strip().lstrip("•*- 1234567890.")
                    defn = parts[1].strip()
                    if 2 < len(term) < 40 and len(defn) > 15:
                        cards.append(Flashcard(
                            front=f"Define: {term}",
                            back=defn,
                            tag="definitions"
                        ))

        # Fallback if no structured definitions
        if len(cards) < 3:
            sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 30]
            for s in sentences[:max_cards]:
                words = s.split()
                if len(words) > 6:
                    key = " ".join(words[:3])
                    cards.append(Flashcard(
                        front=f"Explain the concept regarding '{key}'...",
                        back=s,
                        tag="concepts"
                    ))

        return cards[:max_cards]

    @classmethod
    def to_tsv(cls, cards: List[Flashcard]) -> str:
        """Exports cards to Anki-compatible TSV format."""
        output = io.StringIO()
        writer = csv.writer(output, delimiter="\t", lineterminator="\n")
        for c in cards:
            writer.writerow([c.front, c.back, c.tag])
        return output.getvalue()
