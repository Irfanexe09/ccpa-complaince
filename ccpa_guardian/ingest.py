import re
import logging
from typing import List, Dict
from pypdf import PdfReader
from ccpa_guardian.config import DEFAULT_STATUTE_PDF

logger = logging.getLogger(__name__)

class StatuteIngestor:
    """Handles parsing and chunking of CCPA legal documents."""
    
    def __init__(self, pdf_path: str = None):
        self.pdf_path = pdf_path or str(DEFAULT_STATUTE_PDF)
        self.sections: List[Dict[str, str]] = []

    def extract_text(self) -> List[Dict[str, str]]:
        """Extracts text and attempts to split by Section numbers."""
        logger.info(f"Extracting text from {self.pdf_path}")
        
        try:
            reader = PdfReader(self.pdf_path)
            full_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
        except Exception as e:
            logger.error(f"Failed to read PDF: {e}")
            raise FileNotFoundError(f"Could not read PDF at {self.pdf_path}")

        # Regex to find sections like "1798.100." or "Section 1798.100."
        pattern = r'(\d{4}\.\d{3}\.?\s)'
        parts = re.split(pattern, full_text)
        
        if len(parts) < 2:
            logger.warning("Regex split failed to find sections. Using fallback chunking.")
            # Fallback to simple chunking if regex fails
            self.sections = [{"content": full_text, "id": "full_statute"}]
            return self.sections

        self.sections = []
        # The first part is usually introduction text
        if parts[0].strip():
            self.sections.append({
                "id": "Introduction",
                "content": parts[0].strip()
            })

        for i in range(1, len(parts), 2):
            section_id = parts[i].strip().rstrip('.')
            content = parts[i+1].strip()
            if content:
                self.sections.append({
                    "id": f"Section {section_id}",
                    "content": content
                })
        
        logger.info(f"Successfully extracted {len(self.sections)} sections.")
        return self.sections

    def get_sections(self) -> List[Dict[str, str]]:
        return self.sections

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ingestor = StatuteIngestor()
    sections = ingestor.extract_text()
    print(f"Extracted {len(sections)} sections.")
