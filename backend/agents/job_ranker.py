"""
Agent 6: Job Ranker and Filter
Applies user filters and ranks jobs by relevance.
"""

from typing import List, Dict
from datetime import datetime, timedelta
import re


class JobRanker:
    """Filters and ranks jobs based on user preferences."""
    
    def __init__(self):
        self.valid_job_types = ['full-time', 'part-time', 'contract', 'temporary', 'internship', 'apprenticeship']
        self.valid_work_modes = ['remote', 'hybrid', 'on-site', 'onsite']
    
    def filter_and_rank(self, jobs: List[Dict], filters: Dict) -> List[Dict]:
        """
        Apply filters and rank jobs.
        
        Args:
            jobs: List of job dictionaries with match_scores
            filters: Dictionary of filter criteria
            
        Returns:
            Filtered and ranked jobs
        """
        filtered_jobs = jobs.copy()
        
        # Apply each filter
        if filters.get('job_types'):
            filtered_jobs = self._filter_by_job_type(filtered_jobs, filters['job_types'])
        
        if filters.get('work_modes'):
            filtered_jobs = self._filter_by_work_mode(filtered_jobs, filters['work_modes'])
        
        if filters.get('date_posted'):
            filtered_jobs = self._filter_by_date(filtered_jobs, filters['date_posted'])
        
        if filters.get('salary_min') is not None or filters.get('salary_max') is not None:
            filtered_jobs = self._filter_by_salary(
                filtered_jobs,
                filters.get('salary_min'),
                filters.get('salary_max')
            )
        
        if filters.get('min_match_score'):
            filtered_jobs = self._filter_by_match_score(filtered_jobs, filters['min_match_score'])
        
        if filters.get('max_distance_miles'):
            filtered_jobs = self._filter_by_distance(filtered_jobs, filters['max_distance_miles'])
        
        # Rank by sort criteria
        sort_by = filters.get('sort_by', 'match_score')  # Default: match score
        filtered_jobs = self._sort_jobs(filtered_jobs, sort_by)
        
        return filtered_jobs
    
    def _filter_by_job_type(self, jobs: List[Dict], job_types: List[str]) -> List[Dict]:
        """Filter by employment type (full-time, part-time, etc.)."""
        if not job_types:
            return jobs
        
        job_types_lower = [jt.lower() for jt in job_types]
        
        filtered = []
        for job in jobs:
            contract_type = job.get('contract_type', '').lower()
            
            # Check if any job type matches
            if any(jt in contract_type for jt in job_types_lower):
                filtered.append(job)
            elif not contract_type or contract_type == 'not specified':
                # Include jobs with unspecified type
                filtered.append(job)
        
        return filtered
    
    def _filter_by_work_mode(self, jobs: List[Dict], work_modes: List[str]) -> List[Dict]:
        """Filter by remote/hybrid/on-site."""
        if not work_modes:
            return jobs
        
        work_modes_lower = [wm.lower() for wm in work_modes]
        
        filtered = []
        for job in jobs:
            description = job.get('description', '').lower()
            title = job.get('title', '').lower()
            combined_text = description + ' ' + title
            
            # Check if any work mode is mentioned
            matches = False
            for mode in work_modes_lower:
                if mode in combined_text:
                    matches = True
                    break
            
            if matches:
                filtered.append(job)
            elif not any(mode in combined_text for mode in ['remote', 'hybrid', 'on-site', 'onsite', 'office']):
                # Include if work mode not specified
                filtered.append(job)
        
        return filtered
    
    def _filter_by_date(self, jobs: List[Dict], date_posted: str) -> List[Dict]:
        """Filter by posting date (last 24h, 3 days, 7 days, etc.)."""
        if not date_posted or date_posted == 'any':
            return jobs
        
        # Define cutoff dates
        now = datetime.now()
        cutoff_map = {
            '24h': now - timedelta(days=1),
            '3days': now - timedelta(days=3),
            '7days': now - timedelta(days=7),
            '14days': now - timedelta(days=14),
            '30days': now - timedelta(days=30)
        }
        
        cutoff = cutoff_map.get(date_posted)
        if not cutoff:
            return jobs
        
        filtered = []
        for job in jobs:
            created_str = job.get('created', '')
            
            try:
                # Try parsing different date formats
                job_date = self._parse_date(created_str)
                
                if job_date and job_date >= cutoff:
                    filtered.append(job)
                elif not created_str:
                    # Include if date not available
                    filtered.append(job)
            except:
                # Include if can't parse date
                filtered.append(job)
        
        return filtered
    
    def _filter_by_salary(self, jobs: List[Dict], min_salary: float, max_salary: float) -> List[Dict]:
        """Filter by salary range."""
        if min_salary is None and max_salary is None:
            return jobs
        
        filtered = []
        for job in jobs:
            job_min = job.get('salary_min')
            job_max = job.get('salary_max')
            
            # If job has no salary info, include it
            if job_min is None and job_max is None:
                filtered.append(job)
                continue
            
            # Check if salary range overlaps with filter
            passes = True
            if min_salary is not None and job_max is not None:
                if job_max < min_salary:
                    passes = False
            
            if max_salary is not None and job_min is not None:
                if job_min > max_salary:
                    passes = False
            
            if passes:
                filtered.append(job)
        
        return filtered
    
    def _filter_by_match_score(self, jobs: List[Dict], min_score: float) -> List[Dict]:
        """Filter by minimum match score."""
        return [job for job in jobs if job.get('match_score', 0) >= min_score]
    
    def _filter_by_distance(self, jobs: List[Dict], max_distance: float) -> List[Dict]:
        """Filter by maximum distance from location."""
        filtered = []
        for job in jobs:
            distance = job.get('distance')
            
            if distance is None:
                # Include jobs without distance info
                filtered.append(job)
            elif distance <= max_distance:
                filtered.append(job)
        
        return filtered
    
    def _sort_jobs(self, jobs: List[Dict], sort_by: str) -> List[Dict]:
        """Sort jobs by specified criterion."""
        if sort_by == 'match_score':
            jobs.sort(key=lambda x: x.get('match_score', 0), reverse=True)
        elif sort_by == 'date':
            jobs.sort(key=lambda x: x.get('created', ''), reverse=True)
        elif sort_by == 'salary':
            jobs.sort(key=lambda x: x.get('salary_max', 0) or 0, reverse=True)
        
        return jobs
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse various date formats."""
        if not date_str:
            return None
        
        # Try ISO format
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            pass
        
        # Try common formats
        formats = [
            '%Y-%m-%d',
            '%Y-%m-%dT%H:%M:%S',
            '%d/%m/%Y',
            '%m/%d/%Y'
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str[:10], fmt)
            except:
                continue
        
        return None


# Example usage
if __name__ == "__main__":
    ranker = JobRanker()
    
    sample_jobs = [
        {'title': 'Job 1', 'match_score': 85, 'contract_type': 'full-time', 'created': '2024-12-15'},
        {'title': 'Job 2', 'match_score': 92, 'contract_type': 'part-time', 'created': '2024-12-10'},
        {'title': 'Job 3', 'match_score': 78, 'contract_type': 'full-time', 'created': '2024-12-16'}
    ]
    
    filters = {
        'job_types': ['full-time'],
        'date_posted': '7days',
        'min_match_score': 80,
        'sort_by': 'match_score'
    }
    
    filtered = ranker.filter_and_rank(sample_jobs, filters)
    print(f"Filtered jobs: {len(filtered)}")
