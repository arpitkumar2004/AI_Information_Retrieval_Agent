import React from 'react';
import { AlertCircle, Info, AlertTriangle, X } from 'lucide-react';
import { ErrorState } from '../types';

interface ErrorMessageProps {
  error: ErrorState;
  onClose: () => void;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ error, onClose }) => {
  const icons = {
    error: <AlertCircle className="h-5 w-5 text-red-400" />,
    warning: <AlertTriangle className="h-5 w-5 text-yellow-400" />,
    info: <Info className="h-5 w-5 text-blue-400" />
  };

  const colors = {
    error: 'bg-red-50 text-red-800',
    warning: 'bg-yellow-50 text-yellow-800',
    info: 'bg-blue-50 text-blue-800'
  };

  if (!error.show) return null;

  return (
    <div className={`rounded-md p-4 ${colors[error.type]} mb-4`}>
      <div className="flex">
        <div className="flex-shrink-0">
          {icons[error.type]}
        </div>
        <div className="ml-3 flex-1">
          <p className="text-sm font-medium">{error.message}</p>
        </div>
        <div className="ml-auto pl-3">
          <div className="-mx-1.5 -my-1.5">
            <button
              onClick={onClose}
              className={`inline-flex rounded-md p-1.5 focus:outline-none focus:ring-2 focus:ring-offset-2 ${
                error.type === 'error' ? 'hover:bg-red-100 focus:ring-red-600' :
                error.type === 'warning' ? 'hover:bg-yellow-100 focus:ring-yellow-600' :
                'hover:bg-blue-100 focus:ring-blue-600'
              }`}
            >
              <X className="h-5 w-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ErrorMessage;