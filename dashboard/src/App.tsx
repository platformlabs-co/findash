
import { Routes, Route, Navigate } from "react-router-dom";
import AdminLayout from "layouts/admin";
import AuthLayout from "layouts/auth";
import { useAuth0 } from "@auth0/auth0-react";
import { LoadingState } from "components/loading/LoadingState";
import { useEffect } from "react";

const App = () => {
  document.body.classList.add("dark");
  const { isAuthenticated, isLoading, error } = useAuth0();

  useEffect(() => {
    if (error) {
      console.error("Auth0 Error:", error);
    }
  }, [error]);

  if (isLoading) {
    return <LoadingState />;
  }

  if (error) {
    return (
      <div className="flex h-screen w-full items-center justify-center bg-navy-900">
        <div className="text-center text-white">
          <p className="text-xl">Unable to load authentication</p>
          <p className="mt-2 text-sm text-gray-400">Please try refreshing the page</p>
        </div>
      </div>
    );
  }

  return (
    <Routes>
      <Route path="auth/*" element={<AuthLayout />} />
      <Route path="admin/*" element={<AdminLayout />} />
      <Route 
        path="/" 
        element={
          isAuthenticated ? (
            <Navigate to="/admin/default" replace />
          ) : (
            <Navigate to="/auth/sign-in" replace />
          )
        } 
      />
    </Routes>
  );
};

export default App;
