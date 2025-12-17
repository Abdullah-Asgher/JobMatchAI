"""
Agent 5: Job-CV Matcher
Calculates similarity scores between CV and job descriptions using TF-IDF.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from typing import Dict, List
import numpy as np


class JobMatcher:
    """Matches jobs to CV using TF-IDF similarity and skill matching."""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=500,
            stop_words='english',
            ngram_range=(1, 2)  # Include bi-grams
        )
    
    def match_jobs(self, cv_data: Dict, jobs: List[Dict]) -> List[Dict]:
        """
        Calculate match scores for all jobs against CV.
        
        Args:
            cv_data: Parsed CV data
            jobs: List of job dictionaries
            
        Returns:
            Jobs with added 'match_score' field (0-100)
        """
        cv_text = self._prepare_cv_text(cv_data)
        
        for job in jobs:
            job_text = self._prepare_job_text(job)
           
            # Calculate TF-IDF similarity
            tfidf_score = self._calculate_tfidf_similarity(cv_text, job_text)
            
            # Calculate skill match score
            skill_score = self._calculate_skill_match(cv_data, job)
            
            # Calculate experience level match
            experience_score = self._calculate_experience_match(cv_data, job)
            
            # Weighted average (TF-IDF: 50%, Skills: 35%, Experience: 15%)
            final_score = (tfidf_score * 0.5) + (skill_score * 0.35) + (experience_score * 0.15)
            
            job['match_score'] = round(final_score, 1)
            job['match_breakdown'] = {
                'tfidf': round(tfidf_score, 1),
                'skills': round(skill_score, 1),
                'experience': round(experience_score, 1)
            }
        
        # Sort by match score (descending)
        jobs.sort(key=lambda x: x.get('match_score', 0), reverse=True)
        
        return jobs
    
    def _prepare_cv_text(self, cv_data: Dict) -> str:
        """Prepare CV text for comparison."""
        text_parts = []
        
        # Add summary
        if cv_data.get('summary'):
            text_parts.append(cv_data['summary'])
        
        # Add experience
        if cv_data.get('experience'):
            text_parts.extend(cv_data['experience'])
        
        # Add skills (emphasize by adding twice)
        if cv_data.get('skills'):
            skills_text = ' '.join(cv_data['skills'])
            text_parts.append(skills_text)
            text_parts.append(skills_text)  # Double weight
        
        # Add education
        if cv_data.get('education'):
            text_parts.extend(cv_data['education'])
        
        return ' '.join(text_parts)
    
    def _prepare_job_text(self, job: Dict) -> str:
        """Prepare job description for comparison."""
        text_parts = []
        
        # Add title (emphasize by adding twice)
        if job.get('title'):
            text_parts.append(job['title'])
            text_parts.append(job['title'])
        
        # Add description
        if job.get('description'):
            # Clean HTML tags if present
            description = re.sub(r'<[^>]+>', '', job['description'])
            text_parts.append(description)
        
        # Add company (for context)
        if job.get('company'):
            text_parts.append(job['company'])
        
        return ' '.join(text_parts)
    
    def _calculate_tfidf_similarity(self, cv_text: str, job_text: str) -> float:
        """Calculate cosine similarity using TF-IDF vectors."""
        try:
            # Fit and transform
            tfidf_matrix = self.vectorizer.fit_transform([cv_text, job_text])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # Convert to percentage
            return similarity * 100
        
        except Exception as e:
            print(f"Error calculating TF-IDF similarity: {e}")
            return 50.0  # Default neutral score
    
    def _calculate_skill_match(self, cv_data: Dict, job: Dict) -> float:
        """Calculate how many job-required skills are in CV."""
        cv_skills = [skill.lower() for skill in cv_data.get('skills', [])]
        cv_text = cv_data.get('raw_text', '').lower()
        
        # Extract skills mentioned in job description
        job_text = job.get('description', '').lower()
        
        # Common technical skills to look for
        common_skills = [
            'python', 'java', 'javascript', 'c++', 'sql', 'nosql', 'mongodb',
            'react', 'angular', 'vue', 'node.js', 'django', 'flask',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git',
            'machine learning', 'data analysis', 'ai', 'deep learning',
            'agile', 'scrum', 'jira', 'excel', 'powerpoint', 'communication',
            'leadership', 'problem solving', 'project management'
        ]
        
        job_required_skills = [skill for skill in common_skills if skill in job_text]
        
        if not job_required_skills:
            return 70.0  # Neutral score if can't extract skills
        
        # Count how many required skills are in CV
        matched_skills = 0
        for skill in job_required_skills:
            if skill in cv_text or skill in ' '.join(cv_skills):
                matched_skills += 1
        
        # Calculate percentage
        match_percentage = (matched_skills / len(job_required_skills)) * 100
        
        return match_percentage
    
    def _calculate_experience_match(self, cv_data: Dict, job: Dict) -> float:
        """Estimate if experience level matches job requirements."""
        # Count years of experience mentioned in CV
        cv_text = cv_data.get('raw_text', '')
        experience_years = self._extract_years_of_experience(cv_text)
        
        # Extract required years from job description
        job_text = job.get('description', '')
        required_years = self._extract_required_years(job_text)
        
        if required_years is None:
            return 75.0  # Neutral score if can't determine
        
        # Score based on how close the experience is
        if experience_years >= required_years:
            # Candidate has enough experience
            if experience_years <= required_years + 3:
                return 100.0  # Perfect match
            else:
                return 85.0  # Overqualified but still good
        else:
            # Candidate has less experience
            gap = required_years - experience_years
            if gap <= 1:
                return 80.0  # Close enough
            elif gap <= 2:
                return 60.0  # Slightly under
            else:
                return 40.0  # Significantly under-qualified
    
    def _extract_years_of_experience(self, text: str) -> int:
        """Extract years of experience from CV text."""
        # Look for patterns like "5 years experience", "5+ years"
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)',
            r'(?:experience|exp).*?(\d+)\+?\s*years?'
        ]
        
        years = []
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            years.extend([int(m) for m in matches])
        
        # Return max years found, or estimate from date ranges
        if years:
            return max(years)
        
        # Alternatively, count date ranges (YYYY - YYYY)
        date_ranges = re.findall(r'(\d{4})\s*[-–]\s*(\d{4}|present|current)', text.lower())
        if date_ranges:
            total_years = sum([
                (2024 if end in ['present', 'current'] else int(end)) - int(start)
                for start, end in date_ranges
            ])
            return max(total_years, 1)
        
        return 2  # Default assumption: 2 years
    
    def _extract_required_years(self, job_text: str) -> int:
        """Extract required years of experience from job description."""
        # Look for patterns like "5+ years required", "minimum 3 years"
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp).*?(?:required|needed|minimum)',
            r'(?:required|needed|minimum).*?(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s*(?:in|of|with)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, job_text.lower())
            if match:
                return int(match.group(1))
        
        # Check for seniority levels
        if any(term in job_text.lower() for term in ['senior', 'lead', 'principal']):
            return 5
        elif any(term in job_text.lower() for term in ['mid-level', 'intermediate']):
            return 3
        elif any(term in job_text.lower() for term in ['junior', 'entry', 'graduate']):
            return 1
        
        return None  # Can't determine


# Example usage
if __name__ == "__main__":
    matcher = JobMatcher()
    
    sample_cv = {
        'raw_text': 'Software engineer with 5 years of experience in Python, Java, and AWS...',
        'skills': ['Python', 'Java', 'AWS', 'Docker'],
        'experience': ['Senior Developer at Tech Corp'],
        'education': ['BS Computer Science']
    }
    
    sample_jobs = [
        {
            'title': 'Python Developer',
            'description': 'Looking for a Python developer with 3+ years experience in AWS and Docker...',
            'company': 'Tech Startup'
        }
    ]
    
    matched_jobs = matcher.match_jobs(sample_cv, sample_jobs)
    print(f"Match Score: {matched_jobs[0]['match_score']}%")
