import { useState } from 'react'

export default function FilterPanel({ onApplyFilters }) {
    const [jobTypes, setJobTypes] = useState([])
    const [workModes, setWorkModes] = useState([])
    const [datePosted, setDatePosted] = useState('any')
    const [salaryMin, setSalaryMin] = useState('')
    const [salaryMax, setSalaryMax] = useState('')
    const [minMatchScore, setMinMatchScore] = useState(60)

    const handleApply = () => {
        onApplyFilters({
            job_types: jobTypes,
            work_modes: workModes,
            date_posted: datePosted,
            salary_min: salaryMin ? parseFloat(salaryMin) : null,
            salary_max: salaryMax ? parseFloat(salaryMax) : null,
            min_match_score: minMatchScore
        })
    }

    const handleClear = () => {
        setJobTypes([])
        setWorkModes([])
        setDatePosted('any')
        setSalaryMin('')
        setSalaryMax('')
        setMinMatchScore(60)
        onApplyFilters({})
    }

    const toggleArrayValue = (arr, value, setter) => {
        if (arr.includes(value)) {
            setter(arr.filter(v => v !== value))
        } else {
            setter([...arr, value])
        }
    }

    return (
        <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Filters</h3>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {/* Job Type */}
                <div>
                    <h4 className="font-medium text-gray-900 mb-2">Job Type</h4>
                    <div className="space-y-2">
                        {['full-time', 'part-time', 'contract', 'internship'].map(type => (
                            <label key={type} className="flex items-center">
                                <input
                                    type="checkbox"
                                    checked={jobTypes.includes(type)}
                                    onChange={() => toggleArrayValue(jobTypes, type, setJobTypes)}
                                    className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                                />
                                <span className="ml-2 text-sm text-gray-700 capitalize">{type}</span>
                            </label>
                        ))}
                    </div>
                </div>

                {/* Work Mode */}
                <div>
                    <h4 className="font-medium text-gray-900 mb-2">Work Mode</h4>
                    <div className="space-y-2">
                        {['remote', 'hybrid', 'on-site'].map(mode => (
                            <label key={mode} className="flex items-center">
                                <input
                                    type="checkbox"
                                    checked={workModes.includes(mode)}
                                    onChange={() => toggleArrayValue(workModes, mode, setWorkModes)}
                                    className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                                />
                                <span className="ml-2 text-sm text-gray-700 capitalize">{mode}</span>
                            </label>
                        ))}
                    </div>
                </div>

                {/* Date Posted */}
                <div>
                    <h4 className="font-medium text-gray-900 mb-2">Date Posted</h4>
                    <div className="space-y-2">
                        {[
                            { value: '24h', label: 'Last 24 hours' },
                            { value: '3days', label: 'Last 3 days' },
                            { value: '7days', label: 'Last 7 days' },
                            { value: '30days', label: 'Last 30 days' },
                            { value: 'any', label: 'Any time' }
                        ].map(option => (
                            <label key={option.value} className="flex items-center">
                                <input
                                    type="radio"
                                    name="datePosted"
                                    value={option.value}
                                    checked={datePosted === option.value}
                                    onChange={(e) => setDatePosted(e.target.value)}
                                    className="w-4 h-4 text-primary-600 border-gray-300 focus:ring-primary-500"
                                />
                                <span className="ml-2 text-sm text-gray-700">{option.label}</span>
                            </label>
                        ))}
                    </div>
                </div>

                {/* Salary Range */}
                <div>
                    <h4 className="font-medium text-gray-900 mb-2">Salary Range (£)</h4>
                    <div className="space-y-2">
                        <input
                            type="number"
                            placeholder="Min"
                            value={salaryMin}
                            onChange={(e) => setSalaryMin(e.target.value)}
                            className="input-field"
                        />
                        <input
                            type="number"
                            placeholder="Max"
                            value={salaryMax}
                            onChange={(e) => setSalaryMax(e.target.value)}
                            className="input-field"
                        />
                    </div>
                </div>

                {/* Match Score */}
                <div className="md:col-span-2">
                    <h4 className="font-medium text-gray-900 mb-2">
                        Minimum Match Score: {minMatchScore}%
                    </h4>
                    <input
                        type="range"
                        min="60"
                        max="100"
                        value={minMatchScore}
                        onChange={(e) => setMinMatchScore(parseInt(e.target.value))}
                        className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                    />
                </div>
            </div>

            <div className="mt-6 flex space-x-3">
                <button onClick={handleApply} className="btn-primary">
                    Apply Filters
                </button>
                <button onClick={handleClear} className="btn-secondary">
                    Clear All
                </button>
            </div>
        </div>
    )
}
