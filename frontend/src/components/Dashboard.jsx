import { useState, useEffect } from 'react'
import axios from 'axios'
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { TrendingUp, Briefcase, Award, Clock, ChevronDown } from 'lucide-react'

const API_BASE = 'http://localhost:8000/api'

export default function Dashboard() {
    const [stats, setStats] = useState(null)
    const [applications, setApplications] = useState([])
    const [loading, setLoading] = useState(true)
    const [currentPage, setCurrentPage] = useState(1)
    const [itemsPerPage, setItemsPerPage] = useState(10)

    const updateApplicationStatus = async (appId, newStatus) => {
        try {
            await axios.put(`${API_BASE}/applications/${appId}/status`, { status: newStatus })
            // Update local state
            setApplications(apps => apps.map(app =>
                app.id === appId ? { ...app, status: newStatus } : app
            ))
        } catch (error) {
            console.error('Error updating status:', error)
        }
    }

    useEffect(() => {
        fetchDashboardData()
    }, [])

    const fetchDashboardData = async () => {
        try {
            const [statsRes, appsRes] = await Promise.all([
                axios.get(`${API_BASE}/dashboard-stats`),
                axios.get(`${API_BASE}/applications`)
            ])

            setStats(statsRes.data.stats)
            setApplications(appsRes.data.applications)
        } catch (error) {
            console.error('Error fetching dashboard data:', error)
        } finally {
            setLoading(false)
        }
    }

    if (loading) {
        return (
            <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            </div>
        )
    }

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold text-gray-900">Application Dashboard</h2>
                <button
                    onClick={fetchDashboardData}
                    className="btn-secondary"
                >
                    Refresh
                </button>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <StatsCard
                    icon={<Briefcase className="w-8 h-8" />}
                    title="Total Applied"
                    value={stats?.total_applications || 0}
                    color="bg-blue-500"
                />

                <StatsCard
                    icon={<Award className="w-8 h-8" />}
                    title="Avg Match Score"
                    value={`${stats?.avg_match_score || 0}%`}
                    color="bg-green-500"
                />

                <StatsCard
                    icon={<Clock className="w-8 h-8" />}
                    title="Last Applied"
                    value={stats?.last_applied ? new Date(stats.last_applied).toLocaleDateString() : 'N/A'}
                    color="bg-purple-500"
                />
            </div>

            {/* Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Applications Over Time */}
                {stats?.applications_over_time?.length > 0 && (
                    <div className="card">
                        <h3 className="text-lg font-semibold text-gray-900 mb-4">Applications Over Time</h3>
                        <ResponsiveContainer width="100%" height={250}>
                            <LineChart data={stats.applications_over_time}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="date" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Line type="monotone" dataKey="count" stroke="#2563EB" strokeWidth={2} />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                )}

                {/* Match Score Distribution */}
                {stats?.match_score_distribution?.length > 0 && (
                    <div className="card">
                        <h3 className="text-lg font-semibold text-gray-900 mb-4">Match Score Distribution</h3>
                        <ResponsiveContainer width="100%" height={250}>
                            <BarChart data={stats.match_score_distribution}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="range" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Bar dataKey="count" fill="#10B981" />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                )}
            </div>

            {/* Recent Applications */}
            {applications.length > 0 && (
                <div className="card">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Applications</h3>
                    <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Job Title
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Company
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Match Score
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Date Applied
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Source
                                    </th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                        Status
                                    </th>
                                </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                                {applications
                                    .slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage)
                                    .map((app, idx) => (
                                        <tr key={idx} className="hover:bg-gray-50">
                                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                                {app.job_title}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                {app.company}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                {app.match_score ? `${Math.round(app.match_score)}%` : 'N/A'}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                {new Date(app.date_applied).toLocaleDateString()}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                {app.source}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap text-sm">
                                                <StatusDropdown
                                                    status={app.status || 'Applied'}
                                                    onChange={(newStatus) => updateApplicationStatus(app.id, newStatus)}
                                                />
                                            </td>
                                        </tr>
                                    ))}
                            </tbody>
                        </table>
                    </div>

                    {/* Pagination Controls */}
                    {applications.length > 0 && (
                        <div className="flex items-center justify-between px-4 py-3 border-t border-gray-200 sm:px-6">
                            <div className="flex items-center">
                                <span className="text-sm text-gray-700">
                                    Showing <span className="font-medium">{(currentPage - 1) * itemsPerPage + 1}</span> to{' '}
                                    <span className="font-medium">
                                        {Math.min(currentPage * itemsPerPage, applications.length)}
                                    </span> of{' '}
                                    <span className="font-medium">{applications.length}</span> results
                                </span>
                                <div className="ml-4 flex items-center">
                                    <label htmlFor="itemsPerPage" className="text-sm text-gray-700 mr-2">
                                        Rows per page:
                                    </label>
                                    <select
                                        id="itemsPerPage"
                                        value={itemsPerPage}
                                        onChange={(e) => {
                                            setItemsPerPage(Number(e.target.value))
                                            setCurrentPage(1)
                                        }}
                                        className="border border-gray-300 rounded-md text-sm px-2 py-1 focus:ring-primary-500 focus:border-primary-500"
                                    >
                                        <option value={10}>10</option>
                                        <option value={25}>25</option>
                                        <option value={50}>50</option>
                                        <option value={100}>100</option>
                                    </select>
                                </div>
                            </div>
                            <div className="flex gap-2">
                                <button
                                    onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                                    disabled={currentPage === 1}
                                    className="px-3 py-1 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    Previous
                                </button>
                                {Array.from({ length: Math.ceil(applications.length / itemsPerPage) }, (_, i) => i + 1)
                                    .filter(page => {
                                        // Show first page, last page, current page, and neighbors
                                        const totalPages = Math.ceil(applications.length / itemsPerPage)
                                        return page === 1 || page === totalPages || Math.abs(page - currentPage) <= 1
                                    })
                                    .map((page, idx, arr) => (
                                        <span key={page}>
                                            {idx > 0 && arr[idx - 1] !== page - 1 && (
                                                <span className="px-2 text-gray-500">...</span>
                                            )}
                                            <button
                                                onClick={() => setCurrentPage(page)}
                                                className={`px-3 py-1 border rounded-md text-sm font-medium ${currentPage === page
                                                        ? 'bg-primary-600 text-white border-primary-600'
                                                        : 'border-gray-300 text-gray-700 bg-white hover:bg-gray-50'
                                                    }`}
                                            >
                                                {page}
                                            </button>
                                        </span>
                                    ))}
                                <button
                                    onClick={() => setCurrentPage(p => Math.min(Math.ceil(applications.length / itemsPerPage), p + 1))}
                                    disabled={currentPage === Math.ceil(applications.length / itemsPerPage)}
                                    className="px-3 py-1 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    Next
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            )}

            {applications.length === 0 && (
                <div className="card text-center py-12">
                    <Briefcase className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">No applications yet</h3>
                    <p className="text-gray-600">Start applying to jobs to see your application dashboard</p>
                </div>
            )}
        </div>
    )
}

function StatsCard({ icon, title, value, color }) {
    return (
        <div className="card">
            <div className="flex items-center">
                <div className={`${color} p-3 rounded-lg text-white mr-4`}>
                    {icon}
                </div>
                <div>
                    <p className="text-sm text-gray-600 font-medium">{title}</p>
                    <p className="text-2xl font-bold text-gray-900">{value}</p>
                </div>
            </div>
        </div>
    )
}

function StatusDropdown({ status, onChange }) {
    const statuses = [
        { value: 'Applied', bgColor: 'bg-blue-100', textColor: 'text-blue-800', borderColor: 'border-blue-300' },
        { value: 'Interview - Phase 1', bgColor: 'bg-yellow-100', textColor: 'text-yellow-800', borderColor: 'border-yellow-300' },
        { value: 'Interview - Phase 2', bgColor: 'bg-orange-100', textColor: 'text-orange-800', borderColor: 'border-orange-300' },
        { value: 'Interview - Final', bgColor: 'bg-purple-100', textColor: 'text-purple-800', borderColor: 'border-purple-300' },
        { value: 'Offer Received', bgColor: 'bg-green-100', textColor: 'text-green-800', borderColor: 'border-green-300' },
        { value: 'Rejected', bgColor: 'bg-red-100', textColor: 'text-red-800', borderColor: 'border-red-300' },
        { value: 'Withdrew', bgColor: 'bg-gray-100', textColor: 'text-gray-800', borderColor: 'border-gray-300' }
    ]

    const currentStatus = statuses.find(s => s.value === status) || statuses[0]

    return (
        <div className="relative inline-block w-48">
            <select
                value={status}
                onChange={(e) => onChange(e.target.value)}
                className={`w-full appearance-none px-3 py-2 pr-8 rounded-lg text-xs font-semibold border-2 cursor-pointer transition-all ${currentStatus.bgColor} ${currentStatus.textColor} ${currentStatus.borderColor} hover:shadow-md focus:ring-2 focus:ring-primary-500 focus:outline-none`}
            >
                {statuses.map(s => (
                    <option key={s.value} value={s.value}>{s.value}</option>
                ))}
            </select>
            <div className={`pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 ${currentStatus.textColor}`}>
                <ChevronDown className="h-4 w-4" />
            </div>
        </div>
    )
}
