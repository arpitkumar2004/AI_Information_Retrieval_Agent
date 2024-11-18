import React from 'react';
import { Search } from 'lucide-react';

interface QueryInputProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  disabled: boolean;
}

const QueryInput: React.FC<QueryInputProps> = ({
  value,
  onChange,
  onSubmit,
  disabled
}) => {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Search Query</h2>
      
      <div className="space-y-4">
        <div>
          <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-1">
            What information would you like to extract?
          </label>
          <div className="relative">
            <input
              type="text"
              id="query"
              value={value}
              onChange={(e) => onChange(e.target.value)}
              placeholder="e.g., Find the email address of {company}"
              className="block w-full rounded-lg border-gray-300 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 pl-4 pr-12 py-3"
            />
          </div>
          <p className="mt-2 text-sm text-gray-500">
            Use {'{company}'} as a placeholder for each entity in your dataset
          </p>
        </div>

        <button
          onClick={onSubmit}
          disabled={disabled}
          className={`w-full flex items-center justify-center px-4 py-3 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white ${
            disabled
              ? 'bg-gray-300 cursor-not-allowed'
              : 'bg-indigo-600 hover:bg-indigo-700'
          } transition-colors`}
        >
          <Search className="w-4 h-4 mr-2" />
          Process Dataset
        </button>
      </div>
    </div>
  );
};

export default QueryInput;