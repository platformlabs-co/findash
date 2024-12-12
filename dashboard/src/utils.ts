

const getBackendUrl = (): string => {
   return process.env.REACT_APP_BACKEND_URL || 'http://localhost:8080';
}

export const CallBackendService = async(path: string, getAccessTokenSilently: () => Promise<string>): Promise<string> => {
  const token = await getAccessTokenSilently();
  try {
    const data = await fetch(getBackendUrl() + path, {
      headers: {
         Authorization: `Bearer ${token}`,
      }
    });
    return data.json();  
   } catch (error) {
    console.error(error);
  }
}