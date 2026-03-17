import re
from pypdf import PdfReader
from typing import List, Dict

class StatuteIngestor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.sections: List[Dict[str, str]] = []

    def extract_text(self):
        """Extracts text and attempts to split by Section numbers."""
        reader = PdfReader(self.pdf_path)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"

        # Regex to find sections like "1798.100." or "Section 1798.100."
        # CCPA statute uses "1798.XXX." format for sections
        pattern = r'(\d{4}\.\d{3}\.?\s)'
        parts = re.split(pattern, full_text)
        
        if len(parts) < 2:
            # Fallback to simple chunking if regex fails
            self.sections = [{"content": full_text, "id": "full_statute"}]
            return

        current_section_id = "Intro"
        for i in range(1, len(parts), 2):
            section_id = parts[i].strip()
            content = parts[i+1].strip()
            self.sections.append({
                "id": f"Section {section_id}",
                "content": content
            })

    def get_sections(self) -> List[Dict[str, str]]:
        return self.sections

if __name__ == "__main__":
    ingestor = StatuteIngestor("/Volumes/MINI 2/ccpa-project/ccpa_statute.pdf")
    ingestor.extract_text()
    sections = ingestor.get_sections()
    print(f"Extracted {len(sections)} sections.")
    if sections:
        print(f"First section: {sections[0]['id']}")
