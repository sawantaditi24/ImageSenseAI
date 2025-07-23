import React, { useState } from 'react';
import './App.css';
import UploadArea from './components/UploadArea';
import StorageUsageComponent from './components/StorageUsage';
import ChatSearch from './components/ChatSearch';
import type { UploadResponse } from './services/api';

function App() {
  const [uploadedFiles, setUploadedFiles] = useState<UploadResponse[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleUploadSuccess = (response: UploadResponse) => {
    setUploadedFiles(prev => [response, ...prev]);
    setSuccess('Screenshot uploaded successfully!');
    setError(null);
    // Clear success message after 3 seconds
    setTimeout(() => setSuccess(null), 3000);
  };

  const handleUploadError = (errorMessage: string) => {
    setError(errorMessage);
    setSuccess(null);
    // Clear error message after 5 seconds
    setTimeout(() => setError(null), 5000);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Image Sense
          </h1>
          <p className="text-lg text-gray-600">
            Upload, categorize, and search your screenshots  with AI
          </p>
        </div>

        {/* Alert Messages */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-800">{error}</p>
              </div>
            </div>
          </div>
        )}

        {success && (
          <div className="mb-6 bg-green-50 border border-green-200 rounded-lg p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-green-800">{success}</p>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Upload Area */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-2xl font-semibold text-gray-900 mb-6">
                Upload Screenshots
              </h2>
              <UploadArea
                onUploadSuccess={handleUploadSuccess}
                onUploadError={handleUploadError}
              />
            </div>

            {/* Recent Uploads */}
            {uploadedFiles.length > 0 && (
              <div className="bg-white rounded-lg shadow p-6 mt-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  Recent Uploads
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  {uploadedFiles.slice(0, 6).map((file, index) => (
                    <div key={index} className="border rounded-lg p-4">
                      <img
                        src={file.data.thumbnail_url}
                        alt={file.data.original_filename}
                        className="w-full h-32 object-cover rounded mb-2"
                      />
                      <p className="text-sm text-gray-600 truncate">
                        {file.data.original_filename}
                      </p>
                      <p className="text-xs text-gray-400">
                        {new Date(file.data.upload_date).toLocaleDateString()}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Chat Search Section */}
            <div className="bg-white rounded-lg shadow p-6 mt-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Search Your Screenshots
              </h3>
              <ChatSearch />
            </div>
          </div>

          {/* Storage Usage */}
          <div className="lg:col-span-1">
            <StorageUsageComponent />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
