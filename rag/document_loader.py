from io import BytesIO

from pypdf import PdfReader


def load_pdf_pages(pdf_bytes: bytes, file_name: str) -> list[dict]:
    """Extract text from a PDF while preserving page numbers."""

    if not pdf_bytes:
        raise ValueError("The uploaded PDF is empty.")

    reader = PdfReader(BytesIO(pdf_bytes))
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            pages.append(
                {
                    "content": text.strip(),
                    "metadata": {
                        "source": file_name,
                        "page": page_number,
                    },
                }
            )

    if not pages:
        raise ValueError(
            "No readable text was found in this PDF. "
            "It may contain scanned pages that require OCR."
        )

    return pages