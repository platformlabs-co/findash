import VendorMetrics from "views/admin/default/components/VendorMetrics";
import DatadogConfig from "views/admin/default/components/DatadogConfig";
import APIConfig from "views/admin/default/components/APIConfig"; // Added import for APIConfig
import { Navigate } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";

const Dashboard = () => {
  const { isAuthenticated, isLoading } = useAuth0();

  if (!isAuthenticated && !isLoading) {
    return <Navigate to="/auth/sign-in" />;
  }
  return (
    <div>
      <div className="mt-5 grid grid-cols-1 gap-5 md:grid-cols-1 lg:grid-cols-3 2xl:grid-cols-2 3xl:grid-cols-2">
        <APIConfig /> {/* Added APIConfig component */}
        <DatadogConfig />
        <VendorMetrics vendorName="datadog"/>
        <VendorMetrics vendorName="aws"/>
        <VendorMetrics vendorName="circleci"/>
        <VendorMetrics vendorName="harness"/>
      </div>
    </div>
  );
};

export default Dashboard;