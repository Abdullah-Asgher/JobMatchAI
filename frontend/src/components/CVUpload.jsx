import { useState, useEffect } from 'react'
import axios from 'axios'
import { Upload, FileText, CheckCircle, AlertCircle, Trash2 } from 'lucide-react'

const API_BASE = 'http://localhost:8000/api'

export default function CVUpload({ existingData, onUploadSuccess, onDeleteCV, onContinueToSearch }) {
    const [file, setFile] = useState(null)
    const [uploading, setUploading] = useState(false)
    const [result, setResult] = useState(existingData || null)
    const [error, setError] = useState(null)
    const [dragActive, setDragActive] = useState(false)
    const [pdfUrl, setPdfUrl] = useState(null)

    // Update result if existingData changes
    useEffect(() => {
        if (existingData) {
            setResult(existingData)
        }
    }, [existingData])

    // Create blob URL when file is uploaded
    useEffect(() => {
        if (file && file.type === 'application/pdf') {
            const url = URL.createObjectURL(file)
            setPdfUrl(url)
            return () => URL.revokeObjectURL(url)
        }
    }, [file])

    const handleDrag = (e) => {
        e.preventDefault()
        e.stopPropagation()
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true)
        } else if (e.type === "dragleave") {
            setDragActive(false)
        }
    }

    const handleDrop = (e) => {
        e.preventDefault()
        e.stopPropagation()
        setDragActive(false)

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0])
        }
    }

    const handleChange = (e) => {
        e.preventDefault()
        if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0])
        }
    }

    const handleFile = (file) => {
        const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        const maxSize = 5 * 1024 * 1024 // 5MB

        if (!validTypes.includes(file.type)) {
            setError('Please upload a PDF or DOCX file')
            return
        }

        if (file.size > maxSize) {
            setError('File size must be less than 5MB')
            return
        }

        setFile(file)
        setError(null)
    }

    const uploadCV = async () => {
        if (!file) return

        setUploading(true)
        setError(null)

        const formData = new FormData()
        formData.append('file', file)

        try {
            const response = await axios.post(`${API_BASE}/upload-cv`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            })

            setResult(response.data)
            // Pass full data to parent to persist
            if (response.data.success && onUploadSuccess) {
                onUploadSuccess(file.name, response.data.ats_result, response.data)
            }
        } catch (err) {
            setError(err.response?.data?.detail || 'Error uploading CV. Please try again.')
        } finally {
            setUploading(false)
        }
    }

    const handleDeleteCV = () => {
        if (pdfUrl) {
            URL.revokeObjectURL(pdfUrl)
        }
        setFile(null)
        setResult(null)
        setError(null)
        setPdfUrl(null)
        if (onDeleteCV) {
            onDeleteCV()
        }
    }

    function onDocumentLoadSuccess({ numPages }) {
        setNumPages(numPages)
    }

    return (
        <div className="max-w-7xl mx-auto space-y-6">
            {/* Upload Area - Always Visible */}
            <div className="card">
                <div className="text-center mb-6">
                    <h2 className="text-3xl font-bold text-gray-900 mb-2">Upload Your CV</h2>
                    <p className="text-gray-600">Get instant ATS score analysis and job matching</p>
                </div>

                {/* Drag and Drop Area */}
                <div
                    className={`border-2 border-dashed rounded-xl p-12 text-center transition-colors ${dragActive
                        ? 'border-primary-500 bg-primary-50'
                        : result ? 'border-green-500 bg-green-50' : 'border-gray-300 hover:border-primary-400'
                        }`}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                >
                    <input
                        type="file"
                        id="cv-upload"
                        className="hidden"
                        accept=".pdf,.docx"
                        onChange={handleChange}
                    />

                    <label htmlFor="cv-upload" className="cursor-pointer">
                        {result ? (
                            <>
                                <CheckCircle className="w-16 h-16 mx-auto text-green-600 mb-4" />
                                <p className="text-lg font-medium text-gray-900 mb-2">
                                    ✓ {result.filename} uploaded successfully
                                </p>
                                <p className="text-sm text-green-600">ATS Score: {result.ats_result?.total_score}/100</p>
                            </>
                        ) : (
                            <>
                                <Upload className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                                <p className="text-lg font-medium text-gray-700 mb-2">
                                    {file ? file.name : 'Drag & drop your CV here'}
                                </p>
                                <p className="text-sm text-gray-500 mb-4">or click to browse</p>
                                <p className="text-xs text-gray-400">Supported: PDF, DOCX (Max 5MB)</p>
                            </>
                        )}
                    </label>
                </div>

                {error && (
                    <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start">
                        <AlertCircle className="w-5 h-5 text-red-600 mt-0.5 mr-3 flex-shrink-0" />
                        <p className="text-sm text-red-800">{error}</p>
                    </div>
                )}

                {file && !result && (
                    <div className="mt-6 flex justify-center">
                        <button
                            onClick={uploadCV}
                            disabled={uploading}
                            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            {uploading ? (
                                <span className="flex items-center">
                                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                    </svg>
                                    Analyzing CV...
                                </span>
                            ) : (
                                'Analyze CV & Find Jobs →'
                            )}
                        </button>
                    </div>
                )}
            </div>

            {/* Upload New CV Button - Shows when CV is uploaded */}
            {result && (
                <div className="flex justify-center">
                    <button
                        onClick={handleDeleteCV}
                        className="btn-secondary flex items-center space-x-2 text-red-600 hover:bg-red-50 border-red-300"
                    >
                        <Trash2 className="w-4 h-4" />
                        <span>Upload New CV</span>
                    </button>
                </div>
            )}

            {/* Two Column Layout - PDF Viewer & ATS Results */}
            {result && (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Left Column: PDF Viewer */}
                    <div className="card">
                        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center">
                            <FileText className="w-5 h-5 mr-2 text-primary-600" />
                            Your CV (Original PDF)
                        </h3>

                        {/* PDF Display */}
                        <div className="bg-gray-100 rounded-lg overflow-hidden border-2 border-gray-300" style={{ height: '700px' }}>
                            {result.filename.toLowerCase().endsWith('.pdf') && pdfUrl ? (
                                <embed
                                    src={pdfUrl}
                                    type="application/pdf"
                                    width="100%"
                                    height="100%"
                                    style={{ border: 'none' }}
                                />
                            ) : (
                                <div className="p-6 h-full overflow-y-auto">
                                    <p className="text-gray-600 mb-4 text-center">
                                        {result.filename.toLowerCase().endsWith('.pdf')
                                            ? 'Loading PDF...'
                                            : 'PDF preview only available for PDF files'}
                                    </p>
                                    <div className="bg-white p-4 rounded border border-gray-200">
                                        <pre className="whitespace-pre-wrap text-sm font-mono text-gray-800">
                                            {result.cv_data?.raw_text || 'No content available'}
                                        </pre>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Right Column: ATS Results */}
                    <div className="card">
                        <h3 className="text-xl font-bold text-gray-900 mb-4">ATS Analysis</h3>
                        <ATSResults result={result.ats_result} onContinueToSearch={onContinueToSearch} />
                    </div>
                </div>
            )}
        </div>
    )
}

// ATS Results Component
function ATSResults({ result, onContinueToSearch }) {
    const getScoreColor = (score) => {
        if (score >= 80) return 'text-green-600'
        if (score >= 70) return 'text-yellow-600'
        return 'text-red-600'
    }

    const getScoreBgColor = (score) => {
        if (score >= 80) return 'bg-green-100'
        if (score >= 70) return 'bg-yellow-100'
        return 'bg-red-100'
    }

    return (
        <div className="space-y-6">
            {/* Score Display */}
            <div className="text-center">
                <div className={`inline-flex items-center space-x-2 px-6 py-3 rounded-full ${getScoreBgColor(result.total_score)}`}>
                    <span className={`text-5xl font-bold ${getScoreColor(result.total_score)}`}>
                        {result.total_score}
                    </span>
                    <span className="text-2xl text-gray-600">/100</span>
                </div>
                <p className="mt-3 text-lg font-medium text-gray-700">{result.grade}</p>
            </div>

            {/* Score Breakdown */}
            <div>
                <h4 className="font-semibold text-gray-900 mb-3">Score Breakdown</h4>
                <div className="grid grid-cols-2 gap-3">
                    {Object.entries(result.score_breakdown).map(([key, value]) => (
                        <div key={key} className="p-3 bg-gray-50 rounded-lg">
                            <p className="text-xs text-gray-600 uppercase tracking-wide mb-1">
                                {key.replace('_', ' ')}
                            </p>
                            <p className="text-xl font-bold text-gray-900">{Math.round(value)}</p>
                        </div>
                    ))}
                </div>
            </div>

            {/* Strengths */}
            {result.strengths.length > 0 && (
                <div>
                    <h4 className="flex items-center font-semibold text-gray-900 mb-2">
                        <CheckCircle className="w-5 h-5 text-green-600 mr-2" />
                        Strengths
                    </h4>
                    <ul className="space-y-2">
                        {result.strengths.map((strength, idx) => (
                            <li key={idx} className="flex items-start text-sm text-gray-700">
                                <span className="text-green-600 mr-2 flex-shrink-0">✓</span>
                                <span>{strength}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Improvements */}
            {result.improvements.length > 0 && (
                <div>
                    <h4 className="flex items-center font-semibold text-gray-900 mb-2">
                        <AlertCircle className="w-5 h-5 text-yellow-600 mr-2" />
                        Improvements
                    </h4>
                    <ul className="space-y-2">
                        {result.improvements.slice(0, 5).map((improvement, idx) => (
                            <li key={idx} className="p-2 bg-yellow-50 border border-yellow-200 rounded text-sm text-gray-700">
                                {improvement}
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Continue Button */}
            <div className="pt-4 border-t border-gray-200">
                <button
                    onClick={onContinueToSearch}
                    className="w-full btn-primary"
                >
                    Continue to Job Search →
                </button>
            </div>
        </div>
    )
}
