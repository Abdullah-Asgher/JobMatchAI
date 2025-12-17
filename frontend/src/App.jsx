import { useState } from 'react'
import CVUpload from './components/CVUpload'
import JobSearch from './components/JobSearch'
import Dashboard from './components/Dashboard'
import { Briefcase } from 'lucide-react'
import './index.css'

function App() {
    const [currentView, setCurrentView] = useState('upload') // upload, search, dashboard
    const [cvFile, setCvFile] = useState(null)
    const [atsResult, setAtsResult] = useState(null)
    const [uploadedCVData, setUploadedCVData] = useState(null) // Store full upload result

    // Job search persistence state
    const [jobSearchState, setJobSearchState] = useState({
        jobs: [],
        searchParams: { jobTitle: '', location: '' },
        filters: {},
        loading: false
    })

    const handleDeleteCV = () => {
        setCvFile(null)
        setAtsResult(null)
        setUploadedCVData(null)
        setCurrentView('upload')
    }

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center h-16">
                        <div className="flex items-center space-x-3">
                            <div className="bg-primary-600 p-2 rounded-lg">
                                <Briefcase className="w-6 h-6 text-white" />
                            </div>
                            <div>
                                <h1 className="text-2xl font-bold text-gray-900">JobMatchAI</h1>
                                <p className="text-xs text-gray-500">AI-Powered Job Search Assistant</p>
                            </div>
                        </div>

                        <nav className="flex space-x-1">
                            <button
                                onClick={() => setCurrentView('upload')}
                                className={`px-4 py-2 rounded-lg font-medium transition-colors ${currentView === 'upload'
                                    ? 'bg-primary-600 text-white'
                                    : 'text-gray-600 hover:bg-gray-100'
                                    }`}
                            >
                                Upload CV
                            </button>
                            <button
                                onClick={() => setCurrentView('search')}
                                className={`px-4 py-2 rounded-lg font-medium transition-colors ${currentView === 'search'
                                    ? 'bg-primary-600 text-white'
                                    : 'text-gray-600 hover:bg-gray-100'
                                    }`}
                            >
                                Search Jobs
                            </button>
                            <button
                                onClick={() => setCurrentView('dashboard')}
                                className={`px-4 py-2 rounded-lg font-medium transition-colors ${currentView === 'dashboard'
                                    ? 'bg-primary-600 text-white'
                                    : 'text-gray-600 hover:bg-gray-100'
                                    }`}
                            >
                                Dashboard
                            </button>
                        </nav>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {currentView === 'upload' && (
                    <CVUpload
                        existingData={uploadedCVData}
                        onUploadSuccess={(file, result, fullData) => {
                            setCvFile(file)
                            setAtsResult(result)
                            setUploadedCVData(fullData)
                        }}
                        onDeleteCV={handleDeleteCV}
                        onContinueToSearch={() => setCurrentView('search')}
                    />
                )}

                {currentView === 'search' && (
                    <JobSearch
                        cvFile={cvFile}
                        atsResult={atsResult}
                        persistedState={jobSearchState}
                        onStateChange={setJobSearchState}
                    />
                )}

                {currentView === 'dashboard' && (
                    <Dashboard />
                )}
            </main>

            {/* Footer */}
            <footer className="bg-white border-t border-gray-200 mt-12">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                    <p className="text-center text-sm text-gray-500">
                        JobMatchAI - CN7050 Coursework Project © 2024
                    </p>
                </div>
            </footer>
        </div>
    )
}

export default App
