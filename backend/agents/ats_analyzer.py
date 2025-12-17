"""
Agent 2: ATS Analyzer
Analyzes CV and provides an ATS compatibility score (0-100).
"""

import re
from typing import Dict, List
import spacy


class ATSAnalyzer:
    """Analyzes CVs for ATS (Applicant Tracking System) compatibility."""
    
    def __init__(self):
        # Load spaCy model for NLP analysis
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            print("Warning: spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Action verbs commonly valued in CVs
        self.action_verbs = [
            'achieved', 'improved', 'managed', 'led', 'developed', 'created',
            'increased', 'decreased', 'implemented', 'launched', 'designed',
            'built', 'established', 'streamlined', 'optimized', 'delivered',
            'spearheaded', 'initiated', 'coordinated', 'executed', 'generated'
        ]
    
    def analyze(self, cv_data: Dict, target_keywords: List[str] = None) -> Dict:
        """
        Analyze CV and return ATS score with breakdown.
        
        Args:
            cv_data: Parsed CV data from CVParser
            target_keywords: Optional list of keywords from job description
            
        Returns:
            Dict with score and detailed feedback
        """
        scores = {}
        
        # 1. Contact Information (10 points)
        scores['contact'] = self._score_contact(cv_data.get('contact', {}))
        
        # 2. Formatting (20 points)
        scores['formatting'] = self._score_formatting(cv_data.get('raw_text', ''))
        
        # 3. Keywords (25 points)
        scores['keywords'] = self._score_keywords(cv_data.get('raw_text', ''), target_keywords)
        
        # 4. Action Verbs (15 points)
        scores['action_verbs'] = self._score_action_verbs(cv_data.get('raw_text', ''))
        
        # 5. Section Structure (15 points)
        scores['structure'] = self._score_structure(cv_data)
        
        # 6. Quantifiable Achievements (15 points)
        scores['achievements'] = self._score_achievements(cv_data.get('raw_text', ''))
        
        # Calculate total score
        total_score = sum(scores.values())
        
        # Generate feedback
        feedback = self._generate_feedback(scores, cv_data, target_keywords)
        
        return {
            'total_score': round(total_score),
            'score_breakdown': scores,
            'strengths': feedback['strengths'],
            'improvements': feedback['improvements'],
            'grade': self._get_grade(total_score)
        }
    
    def _score_contact(self, contact: Dict) -> float:
        """Score: 10 points for complete contact information."""
        score = 0
        if contact.get('email'):
            score += 4
        if contact.get('phone'):
            score += 3
        if contact.get('linkedin'):
            score += 3
        return score
    
    def _score_formatting(self, text: str) -> float:
        """Score: 20 points for ATS-friendly formatting."""
        score = 20.0
        
        # Penalize if text is too short (likely poor extraction = complex formatting)
        if len(text) < 500:
            score -=  5
        
        # Check for problematic elements
        if re.search(r'[\|\╣\═\║]', text):  # Table characters
            score -= 8
        
        # Check for reasonable line breaks
        lines = text.split('\n')
        if len(lines) < 20:  # Too few lines = might be in columns/tables
            score -= 4
        
        return max(0, score)
    
    def _score_keywords(self, text: str, target_keywords: List[str] = None) -> float:
        """Score: 25 points for keyword presence."""
        if not target_keywords:
            # Use generic high-value keywords if no job description provided
            target_keywords = [
                'python', 'java', 'javascript', 'sql', 'aws', 'azure',
                'machine learning', 'data analysis', 'project management',
                'leadership', 'communication', 'problem solving'
            ]
        
        text_lower = text.lower()
        found_keywords = sum(1 for keyword in target_keywords if keyword.lower() in text_lower)
        
        if len(target_keywords) == 0:
            return 25.0
        
        keyword_percentage = (found_keywords / len(target_keywords)) * 100
        score = (keyword_percentage / 100) * 25
        
        return min(score, 25.0)
    
    def _score_action_verbs(self, text: str) -> float:
        """Score: 15 points for use of strong action verbs."""
        text_lower = text.lower()
        verb_count = sum(1 for verb in self.action_verbs if verb in text_lower)
        
        # Score based on frequency
        if verb_count >= 10:
            return 15.0
        elif verb_count >= 7:
            return 12.0
        elif verb_count >= 4:
            return 9.0
        elif verb_count >= 2:
            return 6.0
        else:
            return 3.0
    
    def _score_structure(self, cv_data: Dict) -> float:
        """Score: 15 points for proper CV structure."""
        score = 0
        
        # Check for key sections
        if cv_data.get('contact'):
            score += 3
        if cv_data.get('summary') and len(cv_data['summary']) > 50:
            score += 3
        if cv_data.get('experience') and len(cv_data['experience']) > 0:
            score += 4
        if cv_data.get('education') and len(cv_data['education']) > 0:
            score += 3
        if cv_data.get('skills') and len(cv_data['skills']) > 0:
            score += 2
        
        return score
    
    def _score_achievements(self, text: str) -> float:
        """Score: 15 points for quantifiable achievements."""
        # Look for numbers/percentages that indicate achievements
        achievement_patterns = [
            r'\d+%',  # Percentages
            r'\$[\d,]+',  # Dollar amounts
            r'\d+\s*(million|thousand|billion)',  # Large numbers
            r'increased.*\d+',  # Numerical improvements
            r'reduced.*\d+',
            r'saved.*\d+',
            r'grew.*\d+'
        ]
        
        text_lower = text.lower()
        achievement_count = 0
        
        for pattern in achievement_patterns:
            matches = re.findall(pattern, text_lower)
            achievement_count += len(matches)
        
        # Score based on quantifiable achievements found
        if achievement_count >= 8:
            return 15.0
        elif achievement_count >= 5:
            return 12.0
        elif achievement_count >= 3:
            return 9.0
        elif achievement_count >= 1:
            return 6.0
        else:
            return 2.0
    
    def _generate_feedback(self, scores: Dict, cv_data: Dict, target_keywords: List[str]) -> Dict:
        """Generate detailed feedback based on scores."""
        strengths = []
        improvements = []
        
        # Contact information feedback
        if scores['contact'] >= 8:
            strengths.append("Complete contact information provided")
        else:
            improvements.append("Add missing contact info (email, phone, LinkedIn)")
        
        # Formatting feedback
        if scores['formatting'] >= 15:
            strengths.append("Good ATS-friendly formatting")
        else:
            improvements.append("Simplify formatting - avoid tables, columns, and graphics")
        
        # Keywords feedback
        if scores['keywords'] >= 18:
            strengths.append("Strong keyword optimization")
        else:
            improvements.append("Add more relevant keywords from job descriptions")
        
        # Action verbs feedback
        if scores['action_verbs'] >= 10:
            strengths.append("Good use of action verbs")
        else:
            improvements.append(f"Use more action verbs like: {', '.join(self.action_verbs[:5])}")
        
        # Structure feedback
        if scores['structure'] >= 12:
            strengths.append("Well-structured CV with all key sections")
        else:
            missing_sections = []
            if not cv_data.get('summary'):
                missing_sections.append("Professional Summary")
            if not cv_data.get('experience'):
                missing_sections.append("Work Experience")
            if not cv_data.get('education'):
                missing_sections.append("Education")
            if missing_sections:
                improvements.append(f"Add these sections: {', '.join(missing_sections)}")
        
        # Achievements feedback
        if scores['achievements'] >= 10:
            strengths.append("Quantifiable achievements included")
        else:
            improvements.append("Add quantifiable achievements (e.g., 'Increased sales by 30%', 'Managed team of 10')")
        
        return {
            'strengths': strengths,
            'improvements': improvements
        }
    
    def _get_grade(self, score: float) -> str:
        """Convert numerical score to letter grade."""
        if score >= 90:
            return "Excellent"
        elif score >= 80:
            return "Very Good"
        elif score >= 70:
            return "Good"
        elif score >= 60:
            return "Fair"
        else:
            return "Needs Improvement"


# Example usage
if __name__ == "__main__":
    analyzer = ATSAnalyzer()
    
    # Sample parsed CV data
    sample_cv = {
        'raw_text': "Sample CV text with some achievements like increased revenue by 25%...",
        'contact': {'email': 'test@example.com', 'phone': '123-456-7890'},
        'experience': ['Job 1', 'Job 2'],
        'education': ['Degree 1'],
        'skills': ['Python', 'Java', 'SQL']
    }
    
    result = analyzer.analyze(sample_cv)
    print(f"ATS Score: {result['total_score']}/100")
    print(f"Grade: {result['grade']}")
