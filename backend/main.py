"""
JobMatchAI FastAPI Backend
Main application file with API endpoints for all agents.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
import shutil
from pathlib import Path

# Import all agents
from agents.cv_parser import CVParser
from agents.ats_analyzer import ATSAnalyzer
from agents.improvement_advisor import ImprovementAdvisor
from agents.job_aggregator import JobAggregator
from agents.job_matcher import JobMatcher
from agents.job_ranker import JobRanker
from agents.cover_letter_generator import CoverLetterGenerator
from agents.application_tracker import ApplicationTracker

# Initialize FastAPI app
app = FastAPI(
    title="JobMatchAI API",
    description="Multi-agent job search and application assistant",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
cv_parser = CVParser()
ats_analyzer = ATSAnalyzer()
improvement_advisor = ImprovementAdvisor()
job_aggregator = JobAggregator()
job_matcher = JobMatcher()
job_ranker = JobRanker()
cover_letter_generator = CoverLetterGenerator()
application_tracker = ApplicationTracker()

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

#  Pydantic models for request/response
class JobSearchRequest(BaseModel):
    job_title: str
    location: str
    radius_miles: int = 20
    filters: Optional[Dict] = None
    max_results: int = 50

class GenerateCoverLetterRequest(BaseModel):
    job: Dict
    cv_file: Optional[str] = None
    tone: str = "professional"

class TrackApplicationRequest(BaseModel):
    job: Dict
    notes: Optional[str] = ""


# API Endpoints

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "JobMatchAI API is running",
        "version": "1.0.0",
        "agents_available": 8
    }


@app.post("/api/upload-cv")
async def upload_cv(file: UploadFile = File(...)):
    """
    Upload and parse CV file.
    Returns parsed CV data and ATS analysis.
    """
    print(f"=== CV Upload Started ===")
    print(f"Filename: {file.filename}")
    
    # Validate file type
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
    
    # Save uploaded file
    file_path = UPLOAD_DIR / file.filename
    try:
        print(f"Saving file to: {file_path}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print(f"File saved successfully")
    except Exception as e:
        print(f"ERROR saving file: {e}")
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    # Parse CV (Agent 1)
    try:
        print(f"Parsing CV...")
        cv_data = cv_parser.parse(str(file_path))
        print(f"CV parsed successfully. Skills found: {len(cv_data.get('skills', []))}")
    except Exception as e:
        print(f"ERROR parsing CV: {e}")
        raise HTTPException(status_code=500, detail=f"Error parsing CV: {str(e)}")
    
    # Analyze ATS score (Agent 2)
    try:
        print(f"Analyzing ATS score...")
        ats_result = ats_analyzer.analyze(cv_data)
        print(f"ATS Score: {ats_result.get('total_score')}")
    except Exception as e:
        print(f"ERROR analyzing CV: {e}")
        raise HTTPException(status_code=500, detail=f"Error analyzing CV: {str(e)}")
    
    # Track CV upload
    try:
        application_tracker.record_cv_upload(file.filename, ats_result['total_score'])
    except Exception as e:
        print(f"WARNING: Could not track CV upload: {e}")
    
    print(f"=== CV Upload Complete ===")
    return {
        "success": True,
        "filename": file.filename,
        "cv_data": cv_data,
        "ats_result": ats_result
    }


@app.post("/api/analyze-cv")
async def analyze_cv(file: UploadFile = File(...), job_title: str = ""):
    """
    Analyze CV and provide improvement suggestions.
    """
    # Parse CV
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    cv_data = cv_parser.parse(str(file_path))
    
    # Analyze ATS (Agent 2)
    ats_result = ats_analyzer.analyze(cv_data, target_keywords=None)
    
    # Get improvement advice (Agent 3)
    advice = improvement_advisor.generate_advice(ats_result, cv_data, job_title)
    
    return {
        "success": True,
        "ats_result": ats_result,
        "advice": advice
    }


@app.post("/api/search-jobs")
async def search_jobs(request: JobSearchRequest, cv_file: Optional[str] = None):
    """
    Search for jobs across multiple APIs and match to CV.
    """
    try:
        # Fetch jobs from APIs (Agent 4)
        jobs = job_aggregator.fetch_all_jobs(
            job_title=request.job_title,
            location=request.location,
            radius_miles=request.radius_miles,
            max_results=request.max_results
        )
        
        if not jobs:
            return {
                "success": True,
                "jobs": [],
                "total_jobs": 0,
                "message": "No jobs found. Try different search criteria."
            }
        
        # If CV is provided, calculate match scores (Agent 5)
        if cv_file:
            cv_path = UPLOAD_DIR / cv_file
            if cv_path.exists():
                cv_data = cv_parser.parse(str(cv_path))
                jobs = job_matcher.match_jobs(cv_data, jobs)
        
        # Apply filters and rank (Agent 6)
        if request.filters:
            jobs = job_ranker.filter_and_rank(jobs, request.filters)
        
        return {
            "success": True,
            "jobs": jobs,
            "total_jobs": len(jobs),
            "filters_applied": request.filters is not None
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching jobs: {str(e)}")


@app.post("/api/generate-cover-letter")
async def generate_cover_letter(request: GenerateCoverLetterRequest):
    """
    Generate personalized cover letter for a job.
    """
    try:
        # Get CV data
        cv_data = {}
        if request.cv_file:
            cv_path = UPLOAD_DIR / request.cv_file
            if cv_path.exists():
                cv_data = cv_parser.parse(str(cv_path))
        
        # Generate cover letter (Agent 7)
        result = cover_letter_generator.generate(cv_data, request.job, request.tone)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating cover letter: {str(e)}")


@app.post("/api/track-application")
async def track_application(request: TrackApplicationRequest):
    """
    Track a job application.
    """
    try:
        # Track application (Agent 8)
        app_id = application_tracker.track_application(request.job, request.notes)
        
        return {
            "success": True,
            "application_id": app_id,
            "message": "Application tracked successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error tracking application: {str(e)}")


@app.get("/api/applications")
async def get_applications():
    """
    Get all tracked applications.
    """
    try:
        applications = application_tracker.get_all_applications()
        
        return {
            "success": True,
            "applications": applications,
            "total": len(applications)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving applications: {str(e)}")


@app.put("/api/applications/{app_id}/status")
async def update_application_status(app_id: int, request: dict):
    """Update the status of an application."""
    try:
        new_status = request.get('status')
        success = application_tracker.update_application_status(app_id, new_status)
        
        if success:
            return {"success": True, "status": new_status}
        else:
            raise HTTPException(status_code=404, detail="Application not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dashboard-stats")
async def get_dashboard_stats():
    """
    Get analytics for dashboard.
    """
    try:
        stats = application_tracker.get_application_stats()
        
        return {
            "success": True,
            "stats": stats
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving stats: {str(e)}")


@app.post("/api/check-applied")
async def check_if_applied(job: Dict):
    """
    Check if user has already applied to this job.
    """
    try:
        has_applied = application_tracker.check_if_applied(job)
        
        return {
            "success": True,
            "has_applied": has_applied
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking application status: {str(e)}")


# Mount uploads directory for static file serving (MUST BE AFTER ALL ROUTES BUT BEFORE if __name__)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
