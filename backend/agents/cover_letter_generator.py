"""
Agent 7: Cover Letter Generator
Generates personalized cover letters using OpenAI GPT-4.
"""

from openai import OpenAI
import os
from typing import Dict
from dotenv import load_dotenv

load_dotenv()


class CoverLetterGenerator:
    """Generates tailored cover letters for job applications using AI."""
    
    def __init__(self):
        """Initialize the cover letter generator with OpenAI."""
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-4o-mini"  # Using gpt-4o-mini for faster, cost-effective generation  # or "gpt-3.5-turbo" for faster/cheaper
    
    def generate(self, cv_data: Dict, job: Dict, tone: str = "professional") -> Dict:
        """
        Generate a personalized cover letter.
        
        Args:
            cv_data: Parsed CV data
            job: Job dictionary
            tone: Tone style ('professional', 'creative', 'technical')
            
        Returns:
            Dict with cover letter text and metadata
        """
        # Construct prompt
        prompt = self._build_prompt(cv_data, job, tone)
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert career advisor and professional cover letter writer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=600
            )
            
            cover_letter_text = response.choices[0].message.content.strip()
            
            return {
                'success': True,
                'cover_letter': cover_letter_text,
                'word_count': len(cover_letter_text.split()),
                'tone': tone,
                'job_title': job.get('title', ''),
                'company': job.get('company', '')
            }
        
        except Exception as e:
            print(f"Error generating cover letter: {e}")
            return {
                'success': False,
                'error': str(e),
                'cover_letter': self._generate_fallback_letter(cv_data, job)
            }
    
    def _build_prompt(self, cv_data: Dict, job: Dict, tone: str) -> str:
        """Build the prompt for GPT-4."""
        # Extract key info from CV
        skills = ', '.join(cv_data.get('skills', [])[:10])
        experience_summary = ' '.join(cv_data.get('experience', [])[:2])[:300]
        education = cv_data.get('education', [])
        education_str = education[0] if education else "relevant education"
        
        # Extract job info
        job_title = job.get('title', 'this position')
        company = job.get('company', 'your company')
        job_description = job.get('description', '')[:500]
        
        # Tone-specific instructions
        tone_instructions = {
            'professional': 'Use a formal, professional tone. Be concise and business-like.',
            'creative': 'Use a warm, engaging tone. Show personality while remaining professional.',
            'technical': 'Use precise technical language. Focus on specific skills and technologies.'
        }
        
        tone_instruction = tone_instructions.get(tone, tone_instructions['professional'])
        
        prompt = f"""Write a compelling cover letter for a job application.

Job Details:
- Position: {job_title}
- Company: {company}
- Job Description: {job_description}

Candidate Information:
- Skills: {skills}
- Recent Experience: {experience_summary}
- Education: {education_str}

Instructions:
- {tone_instruction}
- Length: 250-350 words
- Structure: Opening paragraph (express interest), body paragraph (highlight relevant skills and experience with specific examples), closing paragraph (call to action)
- Personalize to {company} and {job_title}
- Mention specific skills from the job description that match the candidate's background
- Do NOT include placeholder text like "[Your Name]" or "[Date]"
- Do NOT include address blocks or formal letter formatting
- Start directly with the content

Cover Letter:"""
        
        return prompt
    
    def _generate_fallback_letter(self, cv_data: Dict, job: Dict) -> str:
        """Generate a basic cover letter if API fails."""
        job_title = job.get('title', 'this position')
        company = job.get('company', 'your company')
        skills = ', '.join(cv_data.get('skills', [])[:5])
        
        return f"""I am writing to express my strong interest in the {job_title} position at {company}. With my background in {skills}, I am confident in my ability to contribute effectively to your team.

Throughout my career, I have developed strong technical and problem-solving skills that align well with the requirements of this role. My experience has equipped me with the ability to work collaboratively, adapt to new challenges, and deliver results in fast-paced environments.

I am particularly drawn to {company} because of its reputation for innovation and excellence. I am excited about the opportunity to bring my skills and enthusiasm to your team and contribute to your continued success.

I would welcome the opportunity to discuss how my background aligns with your needs. Thank you for considering my application.

Sincerely,
[Your Name]"""


# Example usage
if __name__ == "__main__":
    generator = CoverLetterGenerator()
    
    sample_cv = {
        'skills': ['Python', 'Java', 'AWS', 'Docker', 'SQL'],
        'experience': [
            'Senior Software Engineer at Tech Corp - Led development of microservices architecture'
        ],
        'education': ['BS Computer Science, University of XYZ']
    }
    
    sample_job = {
        'title': 'Senior Python Developer',
        'company': 'Innovative Tech Ltd',
        'description': 'We are seeking an experienced Python developer with AWS and Docker experience...'
    }
    
    result = generator.generate(sample_cv, sample_job, tone='professional')
    
    if result['success']:
        print(result['cover_letter'])
        print(f"\nWord count: {result['word_count']}")
