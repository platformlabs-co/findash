interface APIResponse<T = any> {
  data?: T;
  error?: {
    message: string;
    status?: number;
  };
}

export const CallBackendService = async <T>(
  endpoint: string,
  getToken: () => Promise<string>,
  options: RequestInit = {}
): Promise<T> => {
  try {
    const token = await getToken();
    const baseUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
    
    const response = await fetch(`${baseUrl}${endpoint}`, {
      ...options,
      headers: {
        ...options.headers,
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      // Handle HTTP errors
      let errorMessage = 'An error occurred';
      try {
        const errorData = await response.json();
        errorMessage = errorData.message || errorData.detail || 'An error occurred';
      } catch {
        errorMessage = response.statusText || 'An error occurred';
      }

      throw {
        message: errorMessage,
        status: response.status,
        response: response, // Include response object for error type checking
      };
    }

    const data = await response.json();
    return data as T;

  } catch (error: any) {
    // Handle network/connection errors
    if (!error.response) {
      throw {
        message: 'Unable to connect to the API server',
        isConnectionError: true,
      };
    }

    // Re-throw HTTP errors
    if (error.status === 401) {
      throw {
        message: 'Authentication failed. Please log in again.',
        status: 401,
        response: error.response,
      };
    }

    if (error.status === 403) {
      throw {
        message: 'You do not have permission to access this resource.',
        status: 403,
        response: error.response,
      };
    }

    if (error.status === 404) {
      throw {
        message: 'The requested resource was not found.',
        status: 404,
        response: error.response,
      };
    }

    if (error.status >= 500) {
      throw {
        message: 'The server encountered an error. Please try again later.',
        status: error.status,
        response: error.response,
      };
    }

    // Re-throw the original error if none of the above conditions match
    throw error;
  }
}; 