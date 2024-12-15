
import VendorMetrics from "views/admin/default/components/VendorMetrics";
import { Navigate } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";

const Dashboard = () => {
  const { isAuthenticated, isLoading } = useAuth0();

  if (!isAuthenticated && !isLoading) {
    return <Navigate to="/auth/sign-in" />;
  }
  return (
    <div>
      <div className="mt-5 grid grid-cols-1 gap-5">
        <VendorMetrics vendorName="datadog"/>
      </div>
    </div>
  );
};

export default Dashboard;
