"""Document and lecture note extractor for StudyGhost."""

from pathlib import Path


class LectureParser:
    """Extracts raw lecture notes, textbooks, and slide text."""

    @staticmethod
    def extract_text(file_path: Path) -> str:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if path.suffix.lower() == ".pdf":
            try:
                import pypdf
                reader = pypdf.PdfReader(str(path))
                pages = [page.extract_text() or "" for page in reader.pages]
                return "\n\n".join(pages).strip()
            except Exception as e:
                raise RuntimeError(f"Error reading PDF: {e}")
        else:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read().strip()
