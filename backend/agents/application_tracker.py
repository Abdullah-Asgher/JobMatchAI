"""
Agent 8: Application Tracker
Tracks job applications using SQLite database and generates analytics.
"""

import sqlite3
from datetime import datetime
from typing import List, Dict
import json


class ApplicationTracker:
    """Tracks job applications and generates analytics."""
    
    def __init__(self, db_path: str = "job_applications.db"):
        self.db_path = db_path
        self._initialize_database()
    
    def _initialize_database(self):
        """Create database tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Applications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT,
                job_title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT,
                salary_range TEXT,
                match_score REAL,
                source TEXT,
                job_url TEXT,
                date_applied TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                status TEXT DEFAULT 'Applied'
            )
        ''')
        
        # Add status column if it doesn't exist (for existing databases)
        try:
            cursor.execute("ALTER TABLE applications ADD COLUMN status TEXT DEFAULT 'Applied'")
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        # CV uploads table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cv_uploads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                ats_score REAL,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def update_application_status(self, app_id: int, status: str) -> bool:
        """Update the status of an application."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE applications 
                SET status = ?
                WHERE id = ?
            ''', (status, app_id))
            
            updated = cursor.rowcount > 0
            conn.commit()
            conn.close()
            
            return updated
        except Exception as e:
            print(f"Error updating application status: {e}")
            return False
    
    def track_application(self, job: Dict, notes: str = "") -> int:
        """
        Record a job application.
        
        Args:
            job: Job dictionary
            notes: Optional notes about the application
            
        Returns:
            Application ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Format salary range
        salary_range = None
        if job.get('salary_min') and job.get('salary_max'):
            salary_range = f"${job['salary_min']:,.0f} - ${job['salary_max']:,.0f}"
        
        cursor.execute('''
            INSERT INTO applications 
            (job_id, job_title, company, location, salary_range, match_score, source, job_url, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            job.get('job_id', ''),
            job.get('title', ''),
            job.get('company', ''),
            job.get('location', ''),
            salary_range,
            job.get('match_score'),
            job.get('source', ''),
            job.get('redirect_url', ''),
            notes
        ))
        
        app_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return app_id
    
    def get_all_applications(self) -> List[Dict]:
        """Retrieve all applications."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM applications
            ORDER BY date_applied DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_application_stats(self) -> Dict:
        """Generate application statistics for dashboard."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total applications
        cursor.execute('SELECT COUNT(*) FROM applications')
        total_applications = cursor.fetchone()[0]
        
        # Average match score
        cursor.execute('SELECT AVG(match_score) FROM applications WHERE match_score IS NOT NULL')
        avg_match_score = cursor.fetchone()[0] or 0
        
        # Last application date
        cursor.execute('SELECT MAX(date_applied) FROM applications')
        last_applied = cursor.fetchone()[0]
        
        # Applications by source
        cursor.execute('''
            SELECT source, COUNT(*) as count
            FROM applications
            GROUP BY source
        ''')
        by_source = dict(cursor.fetchall())
        
        # Applications over time (last 7 days)
        cursor.execute('''
            SELECT DATE(date_applied) as date, COUNT(*) as count
            FROM applications
            WHERE date_applied >= datetime('now', '-7 days')
            GROUP BY DATE(date_applied)
            ORDER BY date
        ''')
        applications_over_time = [
            {'date': row[0], 'count': row[1]}
            for row in cursor.fetchall()
        ]
        
        # Match score distribution
        cursor.execute('''
            SELECT 
                CASE 
                    WHEN match_score >= 90 THEN '90-100%'
                    WHEN match_score >= 80 THEN '80-89%'
                    WHEN match_score >= 70 THEN '70-79%'
                    ELSE 'Below 70%'
                END as range,
                COUNT(*) as count
            FROM applications
            WHERE match_score IS NOT NULL
            GROUP BY range
            ORDER BY range DESC
        ''')
        match_score_distribution = [
            {'range': row[0], 'count': row[1]}
            for row in cursor.fetchall()
        ]
        
        # Top companies applied to
        cursor.execute('''
            SELECT company, COUNT(*) as count
            FROM applications
            GROUP BY company
            ORDER BY count DESC
            LIMIT 5
        ''')
        top_companies = [
            {'company': row[0], 'count': row[1]}
            for row in cursor.fetchall()
        ]
        
        conn.close()
        
        return {
            'total_applications': total_applications,
            'avg_match_score': round(avg_match_score, 1),
            'last_applied': last_applied,
            'by_source': by_source,
            'applications_over_time': applications_over_time,
            'match_score_distribution': match_score_distribution,
            'top_companies': top_companies
        }
    
    def check_if_applied(self, job: Dict) -> bool:
        """Check if already applied to this job."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM applications
            WHERE job_title = ? AND company = ?
        ''', (job.get('title', ''), job.get('company', '')))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count > 0
    
    def record_cv_upload(self, filename: str, ats_score: float) -> int:
        """Record a CV upload."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO cv_uploads (filename, ats_score)
            VALUES (?, ?)
        ''', (filename, ats_score))
        
        cv_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return cv_id
    
    def export_to_csv(self, filepath: str):
        """Export applications to CSV file."""
        import csv
        
        applications = self.get_all_applications()
        
        if not applications:
            return
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = applications[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for app in applications:
                writer.writerow(app)
    
    def clear_all_applications(self):
        """Clear all applications from database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM applications')
        
        conn.commit()
        conn.close()


# Example usage
if __name__ == "__main__":
    tracker = ApplicationTracker()
    
    # Track a sample application
    sample_job = {
        'job_id': 'job123',
        'title': 'Software Engineer',
        'company': 'Tech Corp',
        'location': 'London',
        'salary_min': 50000,
        'salary_max': 70000,
        'match_score': 85.5,
        'source': 'Adzuna',
        'redirect_url': 'https://example.com/job123'
    }
    
    app_id = tracker.track_application(sample_job, notes="Applied via company website")
    print(f"Application tracked with ID: {app_id}")
    
    # Get statistics
    stats = tracker.get_application_stats()
    print(f"\nTotal applications: {stats['total_applications']}")
    print(f"Average match score: {stats['avg_match_score']}%")
