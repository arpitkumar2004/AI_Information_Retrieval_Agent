import React, { useState, useCallback } from 'react';
import { Upload, Search, Download, FileSpreadsheet, RefreshCw, AlertCircle } from 'lucide-react';
import FileUpload from './components/FileUpload';
import QueryInput from './components/QueryInput';
import ResultsTable from './components/ResultsTable';
import ErrorMessage from './components/ErrorMessage';
import Papa from 'papaparse'; // CSV parsing library
import { ProcessingStatus, Result, ErrorState } from './types';

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [query, setQuery] = useState('');
  const [status, setStatus] = useState<ProcessingStatus>('idle');
  const [results, setResults] = useState<Result[]>([]);
  const [error, setError] = useState<ErrorState>({
    show: false,
    message: '',
    type: 'error'
  });
  const [logs, setLogs] = useState<log[] | null>(null);
  const [columns, setColumns] = useState<string[]>([]);
  const [selectedColumn, setSelectedColumn] = useState<string>('');

  const handleError = useCallback((message: string, type: 'error' | 'warning' | 'info' = 'error') => {
    setError({
      show: true,
      message,
      type
    });
  }, []);

  const clearError = useCallback(() => {
    setError({
      show: false,
      message: '',
      type: 'error'
    });
  }, []);

  const handleFileUpload = useCallback((uploadedFile: File | null) => {
    setFile(uploadedFile);
    setStatus('idle');
    setResults([]);
    clearError();
    setColumns([]); // Reset columns when a new file is uploaded
    setSelectedColumn(''); // Reset selected column

    if (uploadedFile) {
      // Read the file content using PapaParse
      Papa.parse(uploadedFile, {
        complete: (result) => {
          if (result.data.length > 0) {
            // Extract column names from the first row of the CSV
            const columns = Object.keys(result.data[0]);
            setColumns(columns);
          }
        },
        header: true, // Use the first row as headers
      });
    }
  }, [clearError]);

  // 
  const handleProcess = async () => {
    // Validate that a file has been uploaded
    if (!file) {
      handleError('Please upload a file');
      return;
    }
  
    if (!query) {
      handleError('Please enter a query');
      return;
    }
  
    // Prepare the form data
    const formData = new FormData();
    formData.append('file', file);
    formData.append('query', query); 
    formData.append('column', selectedColumn);
  
    setStatus('processing');
    clearError();
  
    try {
      const response = await fetch('http://127.0.0.1:5000/api/process', {
        method: 'POST',
        body: formData,
      });
  
      // Handle response status
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }
  
      const data = await response.json();
  
      // Validate response structure (ensuring it meets expected format)
      if (!data || !data.results || !Array.isArray(data.results)) {
        throw new Error('Unexpected response structure from server');
      }
  
      // Handle the results and logs
      setResults(data.results);
      setLogs(data.logs);  // If logs need to be displayed on the frontend
      setStatus('completed');
    } catch (err) {
      console.error('Error during processing:', err);
      setStatus('error');
      handleError('An error occurred while processing your request. Please try again.');
    }
  };
  

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            AI Information Retrieval Agent
          </h1>
          <p className="text-gray-600">
            Upload your dataset and let AI extract the information you need
          </p>
        </header>

        <ErrorMessage error={error} onClose={clearError} />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="space-y-6">
            <FileUpload 
              onFileUpload={handleFileUpload} 
              file={file} 
              onError={handleError}
            />
            
            {/* Display the dropdown for selecting a column if CSV has been uploaded */}
            {columns.length > 0 && (
              <div className="mb-6">
                <label htmlFor="column-select" className="block text-sm font-medium text-gray-700">
                  Select Column for Query
                </label>
                <select
                  id="column-select"
                  value={selectedColumn}
                  onChange={(e) => setSelectedColumn(e.target.value)}
                  disabled={!file || status === 'processing'}
                  className="mt-2 block w-full p-2 border border-gray-300 rounded-md shadow-sm"
                >
                  <option value="">Select a column</option>
                  {columns.map((column) => (
                    <option key={column} value={column}>
                      {column}
                    </option>
                  ))}
                </select>
              </div>
            )}

            <QueryInput 
              value={query} 
              onChange={setQuery}
              onSubmit={handleProcess}
              disabled={!file || !selectedColumn || status === 'processing'}
            />
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-800">Processing Status</h2>
              {status === 'processing' && (
                <RefreshCw className="w-5 h-5 text-indigo-600 animate-spin" />
              )}
            </div>
            
            {status === 'idle' && !file && (
              <div className="flex items-center justify-center h-48 text-gray-400">
                <p>Upload a file to begin</p>
              </div>
            )}

            {status === 'processing' && (
              <div className="flex flex-col items-center justify-center h-48 space-y-4">
                <RefreshCw className="w-8 h-8 text-indigo-600 animate-spin" />
                <p className="text-gray-600">Processing your request...</p>
              </div>
            )}

            {status === 'completed' && results.length > 0 && (
              <ResultsTable results={results} />
            )}

            {status === 'error' && (
              <div className="flex items-center justify-center h-48 text-red-500 space-x-2">
                <AlertCircle className="w-6 h-6" />
                <p>An error occurred during processing</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
