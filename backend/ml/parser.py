import os
import io
import PyPDF2
import docx
from typing import Optional

class ResumeParser:
    """
    Parses resume files (PDF and DOCX) to extract text for NLP processing.
    """

    @staticmethod
    def parse_pdf(file_bytes: bytes) -> str:
        """
        Extracts text from a PDF file.
        """
        try:
            reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            return ""

    @staticmethod
    def parse_docx(file_bytes: bytes) -> str:
        """
        Extracts text from a DOCX file.
        """
        try:
            doc = docx.Document(io.BytesIO(file_bytes))
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            print(f"Error parsing DOCX: {e}")
            return ""

    def parse(self, file_content: bytes, filename: str) -> Optional[str]:
        """
        Detects file type and parses accordingly.
        """
        ext = os.path.splitext(filename)[1].lower()
        if ext == '.pdf':
            return self.parse_pdf(file_content)
        elif ext in ['.docx', '.doc']:
            return self.parse_docx(file_content)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
