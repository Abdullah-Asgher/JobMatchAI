# JobMatchAI Frontend

React application for the JobMatchAI job search assistant.

## Setup

```bash
npm install
npm run dev
```

## Features

- CV Upload with drag-and-drop
- ATS Score Analysis
- Job Search with multiple APIs
- Advanced Filtering
- AI-Generated Cover Letters
- Application Tracking
- Analytics Dashboard

## Tech Stack

- React 18
- Vite
- Tailwind CSS
- Axios (API calls)
- Recharts (analytics)
- Lucide React (icons)

## Architecture

- `App.jsx` - Main application with navigation
- `components/CVUpload.jsx` - CV upload and ATS analysis
- `components/JobSearch.jsx` - Job search with filters
- `components/FilterPanel.jsx` - Advanced job filters
- `components/JobCard.jsx` - Individual job display
- `components/CoverLetterModal.jsx` - Cover letter generation
- `components/Dashboard.jsx` - Application analytics

## API Configuration

Backend API runs on `http://localhost:8000/api`

Update `API_BASE` constant in components if backend URL changes.
