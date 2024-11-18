import React, { useCallback } from 'react';
import { Upload, File, X } from 'lucide-react';

interface FileUploadProps {
  onFileUpload: (file: File | null) => void;
  file: File | null;
  onError: (message: string) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileUpload, file, onError }) => {
  const handleDrop = useCallback(
    (e: React.DragEvent<HTMLDivElement>) => {
      e.preventDefault();
      const droppedFile = e.dataTransfer.files[0];

      if (!droppedFile) {
        onError('No file was dropped');
        return;
      }

      if (!droppedFile.type && !droppedFile.name.endsWith('.csv')) {
        onError('Please upload a valid CSV file');
        return;
      }

      if (droppedFile.size > 5 * 1024 * 1024) {
        onError('File size should be less than 5MB');
        return;
      }

      onFileUpload(droppedFile);
    },
    [onFileUpload, onError]
  );

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];

    if (!selectedFile) {
      onError('No file was selected');
      return;
    }

    if (!selectedFile.type && !selectedFile.name.endsWith('.csv')) {
      onError('Please upload a valid CSV file');
      return;
    }

    if (selectedFile.size > 5 * 1024 * 1024) {
      onError('File size should be less than 5MB');
      return;
    }

    onFileUpload(selectedFile);
  };

  const handleClearFile = () => {
    onFileUpload(null);
  };

  return (
    <div
      className="bg-white rounded-xl shadow-lg p-6 w-full"
      // Allow dragging files anywhere on the page
      onDragOver={(e) => e.preventDefault()}
      onDrop={handleDrop}
    >
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Upload Dataset</h2>

      {/* Show file drop zone */}
      {!file ? (
        <div
          onClick={() => document.getElementById('file-input')?.click()} // Make the entire container clickable
          className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-indigo-500 transition-colors cursor-pointer"
        >
          <Upload className="mx-auto h-12 w-12 text-gray-400" />
          <p className="mt-4 text-sm text-gray-600">
            Drag and drop your CSV file here, or{' '}
            <span className="text-indigo-600 hover:text-indigo-500 cursor-pointer">
              browse
            </span>
            <input
              type="file"
              id="file-input"
              className="hidden"
              accept=".csv"
              onChange={handleFileInput}
            />
          </p>
          <p className="mt-2 text-xs text-gray-500">
            Maximum file size: 5MB
          </p>
        </div>
      ) : (
        // Display uploaded file info
        <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
          <div className="flex items-center space-x-3">
            <File className="h-6 w-6 text-indigo-600" />
            <div>
              <p className="text-sm font-medium text-gray-900">{file.name}</p>
              <p className="text-xs text-gray-500">
                {(file.size / 1024).toFixed(2)} KB
              </p>
            </div>
          </div>
          <button
            onClick={handleClearFile}
            className="p-1 hover:bg-gray-200 rounded-full transition-colors"
            aria-label="Remove file"
          >
            <X className="h-5 w-5 text-gray-500" />
          </button>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
