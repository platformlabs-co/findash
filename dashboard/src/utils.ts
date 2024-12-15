

const getBackendUrl = (): string => {
   return process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
}

export const CallBackendService = async(path: string, getAccessTokenSilently: () => Promise<string>, options: RequestInit = {}): Promise<any> => {
  const token = await getAccessTokenSilently();
  try {
    const data = await fetch(getBackendUrl() + path, {
      ...options,
      headers: {
         Authorization: `Bearer ${token}`,
         ...options.headers,
      }
    });
    return data.json();  
   } catch (error) {
    console.error(error);
    throw error;
  }
}