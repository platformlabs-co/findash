import { Routes, Route, Navigate } from "react-router-dom";

import AdminLayout from "layouts/admin";
import AuthLayout from "layouts/auth";

import { useAuth0 } from "@auth0/auth0-react";


const App = () => {
  document.body.classList.add("dark");
  const { isAuthenticated, isLoading } = useAuth0();
  const nav = () => {
    if (isLoading) {
      return <div>Loading...</div>;
    }
    if (isAuthenticated &&!isLoading) {
      return <Navigate to="/admin/default" />;
    }
    return <Navigate to="/auth/sign-in" />;
  };

  return (
    <Routes>
      <Route path="auth/*" element={<AuthLayout />} />
      <Route path="admin/*" element={<AdminLayout />} />
      <Route path="/" element={nav()} />
    </Routes>
  );
};

export default App;