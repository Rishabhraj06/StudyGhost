"""Exam MCQ Simulator with automated distractors and explanations."""

import re
from dataclasses import dataclass
from typing import List


@dataclass
class Question:
    id: int
    prompt: str
    options: List[str]
    correct_idx: int
    explanation: str


class MCQGenerator:
    """Generates multiple-choice exam simulation questions from text."""

    @classmethod
    def generate_questions(cls, text: str, count: int = 5) -> List[Question]:
        sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 35]
        questions: List[Question] = []

        for idx, sentence in enumerate(sentences[:count], 1):
            words = re.findall(r"\b[A-Za-z]{4,}\b", sentence)
            if not words:
                continue

            # Pick a target keyword for cloze deletion
            target_word = words[len(words) // 2]
            prompt = re.sub(r"\b" + re.escape(target_word) + r"\b", "_______", sentence, count=1)

            correct = target_word.capitalize()
            distractors = ["Redundancy", "Throughput", "Latency", "Consensus", "Bandwidth"]
            distractors = [d for d in distractors if d.lower() != correct.lower()][:3]

            options = [correct] + distractors
            # Deterministic pseudo-shuffle based on sentence length
            rot = len(sentence) % 4
            options = options[rot:] + options[:rot]
            correct_idx = options.index(correct)

            questions.append(Question(
                id=idx,
                prompt=f"Question #{idx}: {prompt}?",
                options=[f"{chr(65+i)}) {opt}" for i, opt in enumerate(options)],
                correct_idx=correct_idx,
                explanation=f"Correct answer is {correct}. Context: \"{sentence}.\""
            ))

        return questions
