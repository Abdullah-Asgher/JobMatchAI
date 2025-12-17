# 🚀 Quick Start Guide

## Get API Keys (15 minutes)

1. **Adzuna** (5 mins): https://developer.adzuna.com/signup
   - Get: App ID + API Key
   
2. **Reed** (3 mins): https://www.reed.co.uk/developers/jobseeker
   - Get: API Key
   
3. **JSearch** (5 mins): https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
   - Get: RapidAPI Key
   - Choose FREE plan

## Configure Environment

Edit `backend/.env` and add your keys:
```
ADZUNA_APP_ID=your_app_id
ADZUNA_API_KEY=your_api_key
REED_API_KEY=your_reed_key
RAPIDAPI_KEY=your_rapidapi_key
OPENAI_API_KEY=your_openai_key
```

## Start the Application

### Backend (Terminal 1):
```bash
cd backend
.\venv\Scripts\activate    # Windows
# or: source venv/bin/activate  # Mac/Linux
python main.py
```
Backend runs on: http://localhost:8000

### Frontend (Terminal 2):
```bash
cd frontend
npm run dev
```
Frontend runs on: http://localhost:3000

## Usage

1. **Upload CV** - Drag and drop your CV (PDF/DOCX)
2. **View ATS Score** - See your score breakdown and improvements
3. **Search Jobs** - Enter job title and location
4. **Filter Results** - Use advanced filters
5. **Generate Cover Letters** - AI-powered personalized letters
6. **Track Applications** - Mark jobs as applied
7. **View Dashboard** - Analytics and insights

## Troubleshooting

- **Port already in use**: Change port in `vite.config.js` (frontend) or `main.py` (backend)
- **API errors**: Check your API keys in `.env` file
- **spaCy model missing**: Run `python -m spacy download en_core_web_sm`

## Architecture

**Backend**: 8-agent system with FastAPI
- CV Parser, ATS Analyzer, Improvement Advisor
- Job Aggregator (3 APIs), Matcher, Ranker
- Cover Letter Generator (GPT-4), Application Tracker

**Frontend**: React + Tailwind CSS
- CV Upload, Job Search, Filters
- Job Cards, Cover Letter Modal, Dashboard

Enjoy! 🎉
