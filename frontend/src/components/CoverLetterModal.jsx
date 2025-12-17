import { useState, useEffect } from 'react'
import axios from 'axios'
import { X, Copy, Download, Loader } from 'lucide-react'

const API_BASE = 'http://localhost:8000/api'

export default function CoverLetterModal({ job, cvFile, onClose }) {
    const [coverLetter, setCoverLetter] = useState(null)
    const [loading, setLoading] = useState(true)
    const [tone, setTone] = useState('professional')

    useEffect(() => {
        generateCoverLetter()
    }, [])

    const generateCoverLetter = async () => {
        setLoading(true)
        try {
            const response = await axios.post(
                `${API_BASE}/generate-cover-letter`,
                { job: job, tone: tone, cv_file: cvFile }
            )

            setCoverLetter(response.data)
        } catch (error) {
            console.error('Error generating cover letter:', error)
            setCoverLetter({
                success: false,
                error: error.response?.data?.detail || 'Failed to generate cover letter'
            })
        } finally {
            setLoading(false)
        }
    }

    const copyToClipboard = () => {
        if (coverLetter?.cover_letter) {
            navigator.clipboard.writeText(coverLetter.cover_letter)
            alert('Copied to clipboard!')
        }
    }

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-xl shadow-2xl max-w-3xl w-full max-h-[90vh] overflow-hidden flex flex-col">
                {/* Header */}
                <div className="p-6 border-b border-gray-200 flex justify-between items-start">
                    <div>
                        <h2 className="text-2xl font-bold text-gray-900 mb-1">Cover Letter</h2>
                        <p className="text-sm text-gray-600">
                            {job.title} at {job.company}
                        </p>
                    </div>
                    <button
                        onClick={onClose}
                        className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                    >
                        <X className="w-6 h-6 text-gray-500" />
                    </button>
                </div>

                {/* Tone Selector */}
                <div className="px-6 py-3 border-b border-gray-200 flex items-center space-x-4">
                    <span className="text-sm font-medium text-gray-700">Tone:</span>
                    {['professional', 'creative', 'technical'].map(t => (
                        <button
                            key={t}
                            onClick={() => {
                                setTone(t)
                                generateCoverLetter()
                            }}
                            className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${tone === t
                                ? 'bg-primary-600 text-white'
                                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                }`}
                        >
                            {t.charAt(0).toUpperCase() + t.slice(1)}
                        </button>
                    ))}
                </div>

                {/* Content */}
                <div className="flex-1 overflow-y-auto p-6">
                    {loading ? (
                        <div className="flex flex-col items-center justify-center h-full">
                            <Loader className="w-12 h-12 text-primary-600 animate-spin mb-4" />
                            <p className="text-gray-600">Generating personalized cover letter...</p>
                        </div>
                    ) : coverLetter?.success ? (
                        <div className="prose max-w-none">
                            <div className="whitespace-pre-wrap text-gray-800 leading-relaxed">
                                {coverLetter.cover_letter}
                            </div>
                            <div className="mt-6 pt-4 border-t border-gray-200 text-sm text-gray-600">
                                <p>Word count: {coverLetter.word_count}</p>
                            </div>
                        </div>
                    ) : (
                        <div className="text-center text-red-600">
                            {coverLetter?.error || 'Failed to generate cover letter'}
                        </div>
                    )}
                </div>

                {/* Footer */}
                {!loading && coverLetter?.success && (
                    <div className="p-6 border-t border-gray-200 flex gap-3">
                        <button
                            onClick={copyToClipboard}
                            className="flex-1 btn-secondary flex items-center justify-center space-x-2"
                        >
                            <Copy className="w-4 h-4" />
                            <span>Copy to Clipboard</span>
                        </button>

                        <button
                            onClick={() => {
                                const blob = new Blob([coverLetter.cover_letter], { type: 'text/plain' })
                                const url = URL.createObjectURL(blob)
                                const a = document.createElement('a')
                                a.href = url
                                a.download = `cover-letter-${job.company}.txt`
                                a.click()
                            }}
                            className="flex-1 btn-primary flex items-center justify-center space-x-2"
                        >
                            <Download className="w-4 h-4" />
                            <span>Download as Text</span>
                        </button>
                    </div>
                )}
            </div>
        </div>
    )
}
