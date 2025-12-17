"""
Agent 1: CV Parser
Extracts structured data from PDF and DOCX files.
"""

import PyPDF2
from docx import Document
import re
from typing import Dict, List, Optional


class CVParser:
    """Parses CV files (PDF/DOCX) and extracts structured information."""
    
    def __init__(self):
        self.sections = {
            'contact': [],
            'summary': [],
            'experience': [],
            'education': [],
            'skills': [],
            'certifications': []
        }
    
    def parse_pdf(self, file_path: str) -> Dict:
        """Extract text from PDF file."""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            return {}
        
        return self.extract_sections(text)
    
    def parse_docx(self, file_path: str) -> Dict:
        """Extract text from DOCX file."""
        text = ""
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Error parsing DOCX: {e}")
            return {}
        
        return self.extract_sections(text)
    
    def extract_sections(self, text: str) -> Dict:
        """Extract different sections from CV text."""
        cv_data = {
            'raw_text': text,
            'contact': self._extract_contact(text),
            'summary': self._extract_summary(text),
            'experience': self._extract_experience(text),
            'education': self._extract_education(text),
            'skills': self._extract_skills(text),
            'total_word_count': len(text.split())
        }
        return cv_data
    
    def _extract_contact(self, text: str) -> Dict:
        """Extract contact information."""
        contact = {}
        
        # Email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        contact['email'] = email_match.group(0) if email_match else None
        
        # Phone
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phone_match = re.search(phone_pattern, text)
        contact['phone'] = phone_match.group(0) if phone_match else None
        
        # LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin_match = re.search(linkedin_pattern, text, re.IGNORECASE)
        contact['linkedin'] = linkedin_match.group(0) if linkedin_match else None
        
        return contact
    
    def _extract_summary(self, text: str) -> str:
        """Extract professional summary/objective."""
        summary_keywords = ['summary', 'objective', 'profile', 'professional summary']
        lines = text.split('\n')
        
        summary_text = ""
        capturing = False
        
        for i, line in enumerate(lines):
            lower_line = line.lower().strip()
            
            # Start capturing after finding summary keyword
            if any(keyword in lower_line for keyword in summary_keywords):
                capturing = True
                continue
            
            # Stop at next section
            if capturing:
                if any(keyword in lower_line for keyword in ['experience', 'education', 'skills', 'work history']):
                    break
                if line.strip():
                    summary_text += line.strip() + " "
        
        return summary_text.strip()[:500]  # Limit to 500 chars
    
    def _extract_experience(self, text: str) -> List[str]:
        """Extract work experience entries."""
        experience_keywords = ['experience', 'work history', 'employment', 'professional experience']
        lines = text.split('\n')
        
        experiences = []
        capturing = False
        current_entry = ""
        
        for line in lines:
            lower_line = line.lower().strip()
            
            if any(keyword in lower_line for keyword in experience_keywords):
                capturing = True
                continue
            
            if capturing:
                # Stop at next major section
                if any(keyword in lower_line for keyword in ['education', 'skills', 'certifications']):
                    if current_entry:
                        experiences.append(current_entry.strip())
                    break
                
                if line.strip():
                    # Detect new job entry (usually has dates or company name)
                    if re.search(r'\d{4}', line):  # Year pattern
                        if current_entry:
                            experiences.append(current_entry.strip())
                            current_entry = line.strip()
                        else:
                            current_entry = line.strip()
                    else:
                        current_entry += " " + line.strip()
        
        return experiences[:5]  # Return top 5 experiences
    
    def _extract_education(self, text: str) -> List[str]:
        """Extract education entries."""
        education_keywords = ['education', 'academic', 'qualifications']
        lines = text.split('\n')
        
        education = []
        capturing = False
        
        for line in lines:
            lower_line = line.lower().strip()
            
            if any(keyword in lower_line for keyword in education_keywords):
                capturing = True
                continue
            
            if capturing:
                if any(keyword in lower_line for keyword in ['experience', 'skills', 'certifications']):
                    break
                
                if line.strip() and (re.search(r'\b(university|college|bachelor|master|phd|degree)\b', line, re.IGNORECASE) or re.search(r'\d{4}', line)):
                    education.append(line.strip())
        
        return education[:3]  # Return top 3 education entries
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from CV."""
        skills_keywords = ['skills', 'technical skills', 'core competencies', 'expertise']
        lines = text.split('\n')
        
        skills = []
        capturing = False
        
        for line in lines:
            lower_line = line.lower().strip()
            
            if any(keyword in lower_line for keyword in skills_keywords):
                capturing = True
                continue
            
            if capturing:
                if any(keyword in lower_line for keyword in ['experience', 'education', 'certifications', 'references']):
                    break
                
                if line.strip():
                    # Split by common delimiters
                    potential_skills = re.split(r'[,•|]', line)
                    for skill in potential_skills:
                        cleaned_skill = skill.strip()
                        if cleaned_skill and len(cleaned_skill) > 2:
                            skills.append(cleaned_skill)
        
        return skills[:20]  # Return top 20 skills
    
    def parse(self, file_path: str) -> Dict:
        """Main parse method - detects file type and parses accordingly."""
        if file_path.lower().endswith('.pdf'):
            return self.parse_pdf(file_path)
        elif file_path.lower().endswith('.docx'):
            return self.parse_docx(file_path)
        else:
            raise ValueError("Unsupported file format. Only PDF and DOCX are supported.")


# Example usage
if __name__ == "__main__":
    parser = CVParser()
    # cv_data = parser.parse("sample_cv.pdf")
    # print(cv_data)
