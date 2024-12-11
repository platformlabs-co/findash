
export const getBackendUrl = (): string => {
   return process.env.REACT_APP_BACKEND_URL || 'http://localhost:8080';
}
