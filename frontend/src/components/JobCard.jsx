import { useState } from 'react'
import axios from 'axios'
import { ExternalLink, MapPin, Briefcase, DollarSign, Check, Mail, Calendar } from 'lucide-react'

const API_BASE = 'http://localhost:8000/api'

export default function JobCard({ job, onViewCoverLetter }) {
    const [applied, setApplied] = useState(false)

    const getMatchColor = (score) => {
        if (score >= 85) return 'bg-green-100 text-green-800 border-green-200'
        if (score >= 70) return 'bg-yellow-100 text-yellow-800 border-yellow-200'
        return 'bg-red-100 text-red-800 border-red-200'
    }

    const handleMarkApplied = async () => {
        try {
            await axios.post(`${API_BASE}/track-application`, {
                job: job,
                notes: ''
            })
            setApplied(true)
        } catch (error) {
            console.error('Error tracking application:', error)
        }
    }

    return (
        <div className="card hover:shadow-md transition-shadow">
            <div className="flex justify-between items-start mb-4">
                <div className="flex-1">
                    <div className="flex items-start justify-between">
                        <div>
                            <h3 className="text-xl font-bold text-gray-900 mb-1">{job.title}</h3>
                            <p className="text-lg text-gray-700">{job.company}</p>
                        </div>

                        {job.match_score && (
                            <div className={`px-4 py-2 rounded-full border-2 ${getMatchColor(job.match_score)}`}>
                                <span className="text-lg font-bold">{Math.round(job.match_score)}%</span>
                                <span className="text-xs ml-1">Match</span>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* Job Details */}
            <div className="flex flex-wrap gap-4 mb-4 text-sm text-gray-600">
                <div className="flex items-center">
                    <MapPin className="w-4 h-4 mr-1.5" />
                    {job.location}
                    {job.distance && <span className="ml-1">({job.distance.toFixed(1)} mi)</span>}
                </div>

                {(job.salary_min || job.salary_max) && (
                    <div className="flex items-center">
                        <DollarSign className="w4 h-4 mr-1.5" />
                        {job.salary_min && job.salary_max
                            ? `£${(job.salary_min / 1000).toFixed(0)}k - £${(job.salary_max / 1000).toFixed(0)}k`
                            : job.salary_min
                                ? `From £${(job.salary_min / 1000).toFixed(0)}k`
                                : `Up to £${(job.salary_max / 1000).toFixed(0)}k`
                        }
                    </div>
                )}

                <div className="flex items-center">
                    <Briefcase className="w-4 h-4 mr-1.5" />
                    {job.contract_type || 'Full-time'}
                </div>

                {job.created && (
                    <div className="flex items-center">
                        <Calendar className="w-4 h-4 mr-1.5" />
                        {new Date(job.created).toLocaleDateString()}
                    </div>
                )}
            </div>

            {/* Description Preview */}
            {job.description && (
                <p className="text-gray-700 text-sm line-clamp-3 mb-4">
                    {job.description.replace(/<[^>]*>/g, '').substring(0, 200)}...
                </p>
            )}

            {/* Skills Matched */}
            {job.match_breakdown && (
                <div className="flex gap-2 mb-4">
                    <span className="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded">
                        Skills: {job.match_breakdown.skills}%
                    </span>
                    <span className="text-xs px-2 py-1 bg-purple-100 text-purple-700 rounded">
                        Experience: {job.match_breakdown.experience}%
                    </span>
                </div>
            )}

            {/* Actions */}
            <div className="flex gap-3 pt-4 border-t border-gray-200">
                <button
                    onClick={onViewCoverLetter}
                    className="flex-1 btn-secondary text-sm flex items-center justify-center space-x-2"
                >
                    <Mail className="w-4 h-4" />
                    <span>View Cover Letter</span>
                </button>

                <a
                    href={job.redirect_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex-1 btn-primary text-sm flex items-center justify-center space-x-2"
                >
                    <ExternalLink className="w-4 h-4" />
                    <span>Apply Now</span>
                </a>

                <button
                    onClick={handleMarkApplied}
                    disabled={applied}
                    className={`px-4 py-2 rounded-lg font-medium transition-colors text-sm ${applied
                        ? 'bg-green-100 text-green-700 cursor-not-allowed'
                        : 'bg-gray-100 hover:bg-gray-200 text-gray-700'
                        }`}
                >
                    {applied ? (
                        <><Check className="w-4 h-4 inline mr-1" />Applied</>
                    ) : (
                        'Mark Applied'
                    )}
                </button>
            </div>

            <div className="mt-2 text-xs text-gray-500">
                Source: {job.source}
            </div>
        </div>
    )
}
