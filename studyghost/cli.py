"""StudyGhost Command Line Interface."""

import argparse
import sys
from pathlib import Path

from studyghost.parser import LectureParser
from studyghost.cheatsheet import CheatSheetEngine
from studyghost.mcq_gen import MCQGenerator
from studyghost.flashcards import FlashcardEngine


def main():
    parser = argparse.ArgumentParser(
        prog="studyghost",
        description="Ghostwrite 1-page cheatsheets, Anki flashcards, and MCQ mock exams."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # cheat command
    cheat_parser = subparsers.add_parser("cheat", help="Generate condensed 1-page cheatsheet")
    cheat_parser.add_argument("file", help="Path to lecture note or textbook (TXT or PDF)")
    cheat_parser.add_argument("--title", default="Exam CheatSheet", help="Title for the summary")

    # mcq command
    mcq_parser = subparsers.add_parser("mcq", help="Generate exam simulation MCQs")
    mcq_parser.add_argument("file", help="Path to study file")
    mcq_parser.add_argument("-n", "--count", type=int, default=5, help="Number of questions")

    # flashcards command
    fc_parser = subparsers.add_parser("cards", help="Generate Anki-compatible flashcards")
    fc_parser.add_argument("file", help="Path to study file")
    fc_parser.add_argument("-o", "--output", help="Optional output TSV file")

    args = parser.parse_args()

    try:
        text = LectureParser.extract_text(Path(args.file))
    except Exception as e:
        print(f"[Error] Failed to read source file: {e}", file=sys.stderr)
        sys.exit(1)

    if args.command == "cheat":
        sheet = CheatSheetEngine.generate(text, subject_title=args.title)
        print("=" * 60)
        print(f"👻 STUDYGHOST 1-PAGE CHEATSHEET: {sheet['title'].upper()}")
        print("=" * 60)
        print("\n[📖 CORE DEFINITIONS]")
        for d in sheet["definitions"]:
            print(f"  • {d}")
        print("\n[⚡ FORMULAS & PROTOCOLS]")
        for r in sheet["rules_and_formulas"]:
            print(f"  • {r}")
        print("\n[🎯 HIGH-YIELD EXAM HIGHLIGHTS]")
        for k in sheet["key_takeaways"]:
            print(f"  • {k}")
        print("=" * 60)

    elif args.command == "mcq":
        questions = MCQGenerator.generate_questions(text, count=args.count)
        print("=" * 60)
        print(f"👻 STUDYGHOST MOCK EXAM ({len(questions)} QUESTIONS)")
        print("=" * 60)
        for q in questions:
            print(f"\n{q.prompt}")
            for opt in q.options:
                print(f"   {opt}")
            print(f"   -> [Answer]: {q.explanation}")
        print("=" * 60)

    elif args.command == "cards":
        cards = FlashcardEngine.generate(text)
        tsv = FlashcardEngine.to_tsv(cards)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(tsv)
            print(f"[StudyGhost] Saved {len(cards)} Anki cards to {args.output}")
        else:
            print(f"Generated {len(cards)} flashcards (Anki TSV format):\n")
            print(tsv)


if __name__ == "__main__":
    main()
