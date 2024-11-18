export type ProcessingStatus = 'idle' | 'processing' | 'completed' | 'error';

export interface Result {
  entity: string;
  email: string;
  status: 'success' | 'error';
  error?: string;
}

export interface ProcessResponse {
  status: 'success' | 'error';
  data?: Result[];
  message?: string;
}

export interface ErrorState {
  show: boolean;
  message: string;
  type: 'error' | 'warning' | 'info';
}