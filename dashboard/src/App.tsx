
import { Routes, Route, Navigate } from "react-router-dom";
import AdminLayout from "layouts/admin";
import AuthLayout from "layouts/auth";
import { useAuth0 } from "@auth0/auth0-react";

const App = () => {
  document.body.classList.add("dark");
  const { isAuthenticated, isLoading } = useAuth0();

  if (isLoading) {
    return <div>Loading...</div>;
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
