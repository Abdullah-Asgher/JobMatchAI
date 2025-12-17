"""
Agent 3: CV Improvement Advisor
Provides actionable suggestions to improve CV based on ATS analysis.
"""

from typing import Dict, List


class ImprovementAdvisor:
    """Generates specific, actionable CV improvement recommendations."""
    
    def __init__(self):
        self.common_keywords = {
            'software_engineer': ['Python', 'Java', 'JavaScript', 'SQL', 'Git', 'AWS', 'Docker', 'REST API', 'Agile', 'CI/CD'],
            'data_scientist': ['Python', 'R', 'Machine Learning', 'SQL', 'Statistics', 'TensorFlow', 'PyTorch', 'Data Visualization', 'Pandas', 'NumPy'],
            'project_manager': ['Agile', 'Scrum', 'Stakeholder Management', 'Risk Management', 'Budgeting', 'JIRA', 'Microsoft Project', 'Leadership'],
            'marketing': ['SEO', 'Google Analytics', 'Content Marketing', 'Social Media', 'Email Marketing', 'Adobe Creative Suite', 'Copywriting'],
            'finance': ['Financial Modeling', 'Excel', 'Accounting', 'Bloomberg', 'Risk Analysis', 'Financial Reporting', 'SAP', 'QuickBooks']
        }
    
    def generate_advice(self, ats_result: Dict, cv_data: Dict, job_title: str = "") -> Dict:
        """
        Generate improvement suggestions based on ATS analysis.
        
        Args:
            ats_result: Results from ATSAnalyzer
            cv_data: Parsed CV data
            job_title: Target job title (optional)
            
        Returns:
            Dict with categorized improvements and priority
        """
        suggestions = {
            'critical': [],  # Must fix (score < 60)
            'important': [],  # Should fix (score 60-80)
            'nice_to_have': []  # Optional improvements (score > 80)
        }
        
        total_score = ats_result['total_score']
        score_breakdown = ats_result['score_breakdown']
        
        # Contact Information
        if score_breakdown['contact'] < 8:
            suggestions['critical'].append({
                'category': 'Contact Information',
                'issue': 'Missing contact details',
                'suggestion': 'Add complete contact information: professional email, phone number, and LinkedIn profile at the top of your CV'
            })
        
        # Formatting
        if score_breakdown['formatting'] < 15:
            suggestions['critical'].append({
                'category': 'Formatting',
                'issue': 'ATS may struggle to read your CV',
                'suggestion': 'Use simple formatting: no tables, columns, text boxes, or graphics. Use standard fonts (Arial, Calibri, Times New Roman). Stick to bullets and clear section headers.'
            })
        
        # Keywords
        if score_breakdown['keywords'] < 18:
            keyword_suggestions = self._get_keyword_suggestions(cv_data, job_title)
            suggestions['important'].append({
                'category': 'Keywords',
                'issue': 'Missing important keywords',
                'suggestion': f"Add these relevant keywords to your experience/skills sections: {', '.join(keyword_suggestions[:8])}"
            })
        
        # Action Verbs
        if score_breakdown['action_verbs'] < 10:
            suggestions['important'].append({
                'category': 'Language',
                'issue': 'Weak verb usage',
                'suggestion': 'Start bullet points with strong action verbs like: achieved, improved, led, developed, increased, implemented, optimized'
            })
        
        # Structure
        if score_breakdown['structure'] < 12:
            structure_fixes = self._get_structure_fixes(cv_data)
            if structure_fixes:
                suggestions['critical'].append({
                    'category': 'Structure',
                    'issue': 'Missing key sections',
                    'suggestion': structure_fixes
                })
        
        # Achievements
        if score_breakdown['achievements'] < 10:
            suggestions['important'].append({
                'category': 'Impact',
                'issue': 'Lack of quantifiable achievements',
                'suggestion': 'Add numbers and metrics to demonstrate impact. Examples: "Increased sales by 30%", "Managed team of 10", "Reduced costs by $50K annually"'
            })
        
        # Additional suggestions based on total score
        if total_score < 60:
            suggestions['critical'].append({
                'category': 'Overall',
                'issue': 'CV needs significant improvement',
                'suggestion': 'Consider using a professional CV template and getting feedback from career services or a mentor'
            })
        
        # Word count
        word_count = cv_data.get('total_word_count', 0)
        if word_count < 300:
            suggestions['important'].append({
                'category': 'Content Length',
                'issue': 'CV is too short',
                'suggestion': 'Expand your experience descriptions. Aim for 400-800 words total (1-2 pages).'
            })
        elif word_count > 1200:
            suggestions['nice_to_have'].append({
                'category': 'Content Length',
                'issue': 'CV is too long',
                'suggestion': 'Condense content to 1-2 pages. Focus on most recent and relevant experience.'
            })
        
        # Skills section
        skills_count = len(cv_data.get('skills', []))
        if skills_count < 5:
            suggestions['important'].append({
                'category': 'Skills',
                'issue': 'Limited skills listed',
                'suggestion': 'Add a dedicated "Skills" section with 8-15 relevant technical and soft skills'
            })
        
        return {
            'total_suggestions': len(suggestions['critical']) + len(suggestions['important']) + len(suggestions['nice_to_have']),
            'priority_breakdown': {
                'critical': len(suggestions['critical']),
                'important': len(suggestions['important']),
                'nice_to_have': len(suggestions['nice_to_have'])
            },
            'suggestions': suggestions,
            'estimated_score_improvement': self._estimate_improvement(total_score, suggestions)
        }
    
    def _get_keyword_suggestions(self, cv_data: Dict, job_title: str) -> List[str]:
        """Suggest missing keywords based on job title."""
        # Determine job category
        job_lower = job_title.lower()
        suggested_keywords = []
        
        if any(term in job_lower for term in ['software', 'developer', 'engineer', 'programmer']):
            suggested_keywords = self.common_keywords['software_engineer']
        elif any(term in job_lower for term in ['data', 'scientist', 'analyst', 'machine learning']):
            suggested_keywords = self.common_keywords['data_scientist']
        elif any(term in job_lower for term in ['project manager', 'program manager', 'scrum master']):
            suggested_keywords = self.common_keywords['project_manager']
        elif any(term in job_lower for term in ['marketing', 'brand', 'content']):
            suggested_keywords = self.common_keywords['marketing']
        elif any(term in job_lower for term in ['finance', 'accounting', 'financial']):
            suggested_keywords = self.common_keywords['finance']
        else:
            # Generic suggestions
            suggested_keywords = ['Leadership', 'Communication', 'Problem Solving', 'Project Management', 'Team Collaboration']
        
        # Filter out keywords already in CV
        cv_text = cv_data.get('raw_text', '').lower()
        missing_keywords = [kw for kw in suggested_keywords if kw.lower() not in cv_text]
        
        return missing_keywords
    
    def _get_structure_fixes(self, cv_data: Dict) -> str:
        """Suggest structural improvements."""
        missing = []
        
        if not cv_data.get('summary') or len(cv_data.get('summary', '')) < 50:
            missing.append('Professional Summary (2-3 sentences describing your expertise)')
        
        if not cv_data.get('experience') or len(cv_data.get('experience', [])) == 0:
            missing.append('Work Experience section with job titles, companies, dates, and achievements')
        
        if not cv_data.get('education') or len(cv_data.get('education', [])) == 0:
            missing.append('Education section with degrees, institutions, and graduation dates')
        
        if not cv_data.get('skills') or len(cv_data.get('skills', [])) < 5:
            missing.append('Skills section listing relevant technical and soft skills')
        
        if missing:
            return f"Add these essential sections: {'; '.join(missing)}"
        
        return ""
    
    def _estimate_improvement(self, current_score: float, suggestions: Dict) -> int:
        """Estimate potential score improvement if suggestions are followed."""
        critical_count = len(suggestions['critical'])
        important_count = len(suggestions['important'])
        
        # Each critical fix ~5 points, important ~3 points
        potential_gain = (critical_count * 5) + (important_count * 3)
        
        # Cap at 100
        estimated_new_score = min(current_score + potential_gain, 100)
        
        return int(estimated_new_score - current_score)


# Example usage
if __name__ == "__main__":
    advisor = ImprovementAdvisor()
    
    # Sample ATS result
    sample_ats_result = {
        'total_score': 65,
        'score_breakdown': {
            'contact': 7,
            'formatting': 18,
            'keywords': 15,
            'action_verbs': 8,
            'structure': 10,
            'achievements': 7
        }
    }
    
    sample_cv = {
        'raw_text': 'Sample CV text...',
        'total_word_count': 450,
        'skills': ['Python', 'Java']
    }
    
    advice = advisor.generate_advice(sample_ats_result, sample_cv, "Software Engineer")
    print(f"Total Suggestions: {advice['total_suggestions']}")
    print(f"Estimated Improvement: +{advice['estimated_score_improvement']} points")
