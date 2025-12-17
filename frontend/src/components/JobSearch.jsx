import { useState, useEffect } from 'react'
import axios from 'axios'
import { Search, MapPin, Sliders, Briefcase, Mail, ExternalLink, Check } from 'lucide-react'
import FilterPanel from './FilterPanel'
import JobCard from './JobCard'
import CoverLetterModal from './CoverLetterModal'

const API_BASE = 'http://localhost:8000/api'

export default function JobSearch({ cvFile, atsResult }) {
    const [jobTitle, setJobTitle] = useState('')
    const [location, setLocation] = useState('')
    const [radiusMiles, setRadiusMiles] = useState(20)
    const [jobs, setJobs] = useState([])
    const [filteredJobs, setFilteredJobs] = useState([])
    const [searching, setSearching] = useState(false)
    const [filters, setFilters] = useState({})
    const [showFilters, setShowFilters] = useState(false)
    const [selectedJob, setSelectedJob] = useState(null)
    const [showCoverLetter, setShowCoverLetter] = useState(false)

    const searchJobs = async () => {
        if (!jobTitle || !location) return

        setSearching(true)
        try {
            const response = await axios.post(`${API_BASE}/search-jobs`, {
                job_title: jobTitle,
                location: location,
                radius_miles: radiusMiles,
                filters: filters,
                max_results: 50
            }, {
                params: cvFile ? { cv_file: cvFile } : {}
            })

            const fetchedJobs = response.data.jobs || []
            setJobs(fetchedJobs)
            setFilteredJobs(fetchedJobs)
        } catch (error) {
            console.error('Error searching jobs:', error)
            alert('Error searching jobs: ' + (error.response?.data?.detail || error.message))
        } finally {
            setSearching(false)
        }
    }

    const applyFilters = (newFilters) => {
        setFilters(newFilters)
        // Filter jobs locally for instant feedback
        let filtered = [...jobs]

        if (newFilters.min_match_score) {
            filtered = filtered.filter(job => (job.match_score || 0) >= newFilters.min_match_score)
        }

        setFilteredJobs(filtered)
    }

    return (
        <div className="space-y-6">
            {/* Search Bar */}
            <div className="card">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Job Title
                        </label>
                        <div className="relative">
                            <Briefcase className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                            <input
                                type="text"
                                value={jobTitle}
                                onChange={(e) => setJobTitle(e.target.value)}
                                placeholder="e.g. Software Engineer"
                                className="input-field pl-10"
                            />
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Location
                        </label>
                        <div className="relative">
                            <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                            <input
                                type="text"
                                value={location}
                                onChange={(e) => setLocation(e.target.value)}
                                placeholder="e.g. London, Canary Wharf"
                                className="input-field pl-10"
                            />
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Radius: {radiusMiles} miles
                        </label>
                        <input
                            type="range"
                            min="5"
                            max="50"
                            value={radiusMiles}
                            onChange={(e) => setRadiusMiles(parseInt(e.target.value))}
                            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                        />
                    </div>
                </div>

                <div className="mt-6 flex justify-between items-center">
                    <button
                        onClick={() => setShowFilters(!showFilters)}
                        className="btn-secondary flex items-center space-x-2"
                    >
                        <Sliders className="w-4 h-4" />
                        <span>{showFilters ? 'Hide' : 'Show'} Filters</span>
                    </button>

                    <button
                        onClick={searchJobs}
                        disabled={searching || !jobTitle || !location}
                        className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {searching ? 'Searching...' : 'Find Jobs →'}
                    </button>
                </div>
            </div>

            {/* Filters */}
            {showFilters && (
                <FilterPanel onApplyFilters={applyFilters} />
            )}

            {/* Results */}
            {filteredJobs.length > 0 && (
                <div>
                    <div className="flex justify-between items-center mb-4">
                        <h2 className="text-xl font-bold text-gray-900">
                            Found {filteredJobs.length} Jobs
                        </h2>
                        <select className="input-field w-48">
                            <option value="match_score">Best Match</option>
                            <option value="date">Most Recent</option>
                            <option value="salary">Highest Salary</option>
                        </select>
                    </div>

                    <div className="space-y-4">
                        {filteredJobs.map((job, idx) => (
                            <JobCard
                                key={idx}
                                job={job}
                                onViewCoverLetter={() => {
                                    setSelectedJob(job)
                                    setShowCoverLetter(true)
                                }}
                            />
                        ))}
                    </div>
                </div>
            )}

            {!searching && filteredJobs.length === 0 && jobs.length === 0 && (
                <div className="card text-center py-12">
                    <Search className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">No jobs yet</h3>
                    <p className="text-gray-600">Enter a job title and location to start searching</p>
                </div>
            )}

            {/* Cover Letter Modal */}
            {showCoverLetter && selectedJob && (
                <CoverLetterModal
                    job={selectedJob}
                    cvFile={cvFile}
                    onClose={() => {
                        setShowCoverLetter(false)
                        setSelectedJob(null)
                    }}
                />
            )}
        </div>
    )
}
