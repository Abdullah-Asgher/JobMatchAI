"""
Agent 4: Job API Aggregator
Fetches jobs from multiple APIs (Adzuna, Reed, JSearch) and normalizes data.
"""

import requests
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class JobAggregator:
    """Aggregates job listings from multiple job search APIs."""
    
    def __init__(self):
        # API credentials from environment
        self.adzuna_app_id = os.getenv('ADZUNA_APP_ID')
        self.adzuna_api_key = os.getenv('ADZUNA_API_KEY')
        self.reed_api_key = os.getenv('REED_API_KEY')
        self.rapidapi_key = os.getenv('RAPIDAPI_KEY')
        
        self.adzuna_base_url = "https://api.adzuna.com/v1/api/jobs/gb/search"
        self.reed_base_url = "https://www.reed.co.uk/api/1.0/search"
        self.jsearch_base_url = "https://jsearch.p.rapidapi.com/search"
    
    def fetch_all_jobs(self, 
                       job_title: str, 
                       location: str, 
                       radius_miles: int = 20,
                       max_results: int = 50) -> List[Dict]:
        """
        Fetch jobs from all available APIs and combine results.
        
        Args:
            job_title: Job title to search for
            location: Location (city or postcode)
            radius_miles: Search radius in miles
            max_results: Maximum number of results per API
            
        Returns:
            List of normalized job dictionaries
        """
        all_jobs = []
        
        # Fetch from each API
        print("Fetching from Adzuna...")
        adzuna_jobs = self.fetch_adzuna(job_title, location, radius_miles, max_results)
        all_jobs.extend(adzuna_jobs)
        
        print("Fetching from Reed...")
        reed_jobs = self.fetch_reed(job_title, location, radius_miles, max_results)
        all_jobs.extend(reed_jobs)
        
        print("Fetching from JSearch (RapidAPI)...")
        jsearch_jobs = self.fetch_jsearch(job_title, location, max_results)
        all_jobs.extend(jsearch_jobs)
        
        print(f"Total jobs fetched: {len(all_jobs)}")
        
        # Remove duplicates based on title + company
        unique_jobs = self._remove_duplicates(all_jobs)
        print(f"Unique jobs after deduplication: {len(unique_jobs)}")
        
        return unique_jobs
    
    def fetch_adzuna(self, job_title: str, location: str, radius_miles: int, max_results: int) -> List[Dict]:
        """Fetch jobs from Adzuna API."""
        if not self.adzuna_app_id or not self.adzuna_api_key:
            print("Adzuna API credentials not found")
            return []
        
        try:
            url = f"{self.adzuna_base_url}/1"
            params = {
                'app_id': self.adzuna_app_id,
                'app_key': self.adzuna_api_key,
                'what': job_title,
                'where': location,
                'distance': radius_miles,
                'results_per_page': min(max_results, 50),
                'content-type': 'application/json'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            jobs = data.get('results', [])
            
            # Normalize Adzuna jobs
            normalized = []
            for job in jobs:
                normalized.append({
                    'source': 'Adzuna',
                    'job_id': job.get('id', ''),
                    'title': job.get('title', ''),
                    'company': job.get('company', {}).get('display_name', 'Unknown'),
                    'location': job.get('location', {}).get('display_name', location),
                    'description': job.get('description', ''),
                    'salary_min': job.get('salary_min'),
                    'salary_max': job.get('salary_max'),
                    'contract_type': job.get('contract_type', 'Not specified'),
                    'created': job.get('created', ''),
                    'redirect_url': job.get('redirect_url', ''),
                    'distance': None  # Adzuna doesn't provide distance
                })
            
            return normalized
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching from Adzuna: {e}")
            return []
    
    def fetch_reed(self, job_title: str, location: str, radius_miles: int, max_results: int) -> List[Dict]:
        """Fetch jobs from Reed API."""
        if not self.reed_api_key:
            print("Reed API key not found")
            return []
        
        try:
            url = self.reed_base_url
            params = {
                'keywords': job_title,
                'location': location,
                'distancefromlocation': radius_miles,
                'resultsToTake': min(max_results, 100)
            }
            
            headers = {
                'Authorization': f'Basic {self.reed_api_key}'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            jobs = data.get('results', [])
            
            # Normalize Reed jobs
            normalized = []
            for job in jobs:
                normalized.append({
                    'source': 'Reed',
                    'job_id': job.get('jobId', ''),
                    'title': job.get('jobTitle', ''),
                    'company': job.get('employerName', 'Unknown'),
                    'location': job.get('locationName', location),
                    'description': job.get('jobDescription', ''),
                    'salary_min': job.get('minimumSalary'),
                    'salary_max': job.get('maximumSalary'),
                    'contract_type': job.get('contractType', 'Not specified'),
                    'created': job.get('date', ''),
                    'redirect_url': job.get('jobUrl', ''),
                    'distance': job.get('distance')
                })
            
            return normalized
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching from Reed: {e}")
            return []
    
    def fetch_jsearch(self, job_title: str, location: str, max_results: int) -> List[Dict]:
        """Fetch jobs from JSearch API (RapidAPI)."""
        if not self.rapidapi_key:
            print("RapidAPI key not found")
            return []
        
        try:
            url = self.jsearch_base_url
            params = {
                'query': f"{job_title} in {location}",
                'page': '1',
                'num_pages': '1',
                'date_posted': 'all'
            }
            
            headers = {
                'X-RapidAPI-Key': self.rapidapi_key,
                'X-RapidAPI-Host': 'jsearch.p.rapidapi.com'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            jobs = data.get('data', [])[:max_results]
            
            # Normalize JSearch jobs
            normalized = []
            for job in jobs:
                # Extract salary if available
                salary_min = None
                salary_max = None
                if job.get('job_salary'):
                    salary_min = job['job_salary'].get('min_salary')
                    salary_max = job['job_salary'].get('max_salary')
                
                normalized.append({
                    'source': 'JSearch',
                    'job_id': job.get('job_id', ''),
                    'title': job.get('job_title', ''),
                    'company': job.get('employer_name', 'Unknown'),
                    'location': job.get('job_city', location),
                    'description': job.get('job_description', ''),
                    'salary_min': salary_min,
                    'salary_max': salary_max,
                    'contract_type': job.get('job_employment_type', 'Not specified'),
                    'created': job.get('job_posted_at_datetime_utc', ''),
                    'redirect_url': job.get('job_apply_link', ''),
                    'distance': None
                })
            
            return normalized
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching from JSearch: {e}")
            return []
    
    def _remove_duplicates(self, jobs: List[Dict]) -> List[Dict]:
        """Remove duplicate jobs based on title and company."""
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            # Create a key from title and company (normalized)
            key = (
                job.get('title', '').lower().strip(),
                job.get('company', '').lower().strip()
            )
            
            if key not in seen and key != ('', ''):
                seen.add(key)
                unique_jobs.append(job)
        
        return unique_jobs


# Example usage
if __name__ == "__main__":
    aggregator = JobAggregator()
    jobs = aggregator.fetch_all_jobs(
        job_title="Software Engineer",
        location="London",
        radius_miles=20,
        max_results=20
    )
    
    print(f"\nFetched {len(jobs)} unique jobs")
    if jobs:
        print(f"\nFirst job: {jobs[0]['title']} at {jobs[0]['company']}")
