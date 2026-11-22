"""Unit tests for StudyGhost engines."""

import pytest
from pathlib import Path
from studyghost.cheatsheet import CheatSheetEngine
from studyghost.mcq_gen import MCQGenerator
from studyghost.flashcards import FlashcardEngine
from studyghost.parser import LectureParser


SAMPLE_TEXT = """
Database Normalization: Normalization is the process of organizing data in a database to reduce redundancy.
First Normal Form (1NF): A relation is in 1NF if and only if all underlying domains contain only atomic values.
Second Normal Form (2NF): A relation is in 2NF if it is in 1NF and no non-prime attribute is dependent on any proper subset of any candidate key.
Third Normal Form (3NF): A relation is in 3NF if it is in 2NF and no non-prime attribute is transitively dependent on the primary key.
Boyce-Codd Normal Form (BCNF): BCNF is a stricter version of 3NF where every determinant must be a candidate key.
ACID Properties: ACID stands for Atomicity, Consistency, Isolation, and Durability.
Throughput is defined as the number of transactions processed per second.
"""


def test_cheatsheet_engine():
    sheet = CheatSheetEngine.generate(SAMPLE_TEXT, subject_title="DBMS Revision")
    assert sheet["title"] == "DBMS Revision"
    assert len(sheet["definitions"]) > 0
    assert any("Normalization" in d for d in sheet["definitions"])


def test_mcq_generator():
    questions = MCQGenerator.generate_questions(SAMPLE_TEXT, count=3)
    assert len(questions) == 3
    q = questions[0]
    assert len(q.options) == 4
    assert 0 <= q.correct_idx <= 3
    assert q.explanation != ""


def test_flashcard_engine():
    cards = FlashcardEngine.generate(SAMPLE_TEXT, max_cards=5)
    assert len(cards) > 0
    tsv = FlashcardEngine.to_tsv(cards)
    assert "\t" in tsv
    assert "studyghost" in tsv or "exam-core" in tsv


def test_parser_plaintext(tmp_path):
    test_file = tmp_path / "notes.txt"
    test_file.write_text("Binary search is an efficient search algorithm with O(log n) time complexity.", encoding="utf-8")
    extracted = LectureParser.extract_text(test_file)
    assert "Binary search" in extracted
