import { useEffect } from "react";
import { Link } from "react-router-dom";
import VendorMetrics from "./components/VendorMetrics";
import { useAPIConfigurations } from "./components/hooks/useAPIConfigurations";
import { LoadingState } from "components/loading/LoadingState";

const Dashboard = () => {
  const { configurations, loading } = useAPIConfigurations();
  
  useEffect(() => {
    document.title = "Dashboard";
  }, []);

  if (loading) {
    return <LoadingState />;
  }

  if (configurations.length === 0) {
    return (
      <div className="mt-3 flex flex-col items-center justify-center">
        <h1 className="text-2xl font-bold text-navy-700 dark:text-white">
          Welcome to FinDash 🚀
        </h1>
        <p className="mt-4 text-gray-600 dark:text-gray-400">
          To get started, you'll need to configure your integrations.
        </p>
        <Link
          to="/admin/configuration"
          className="mt-6 rounded-xl bg-brand-500 px-6 py-3 text-white hover:bg-brand-600"
        >
          Configure Vendors
        </Link>
      </div>
    );
  }

  return (
    <div className="mt-3">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {configurations.map((config) => {
          if (config.type === "datadog") {
            return (
              <VendorMetrics
                key={config.id}
                vendor="datadog"
                title="Datadog Metrics"
              />
            );
          }
          if (config.type === "aws") {
            return (
              <VendorMetrics
                key={config.id}
                vendor="aws"
                title="AWS Metrics"
              />
            );
          }
          return null;
        })}
      </div>
    </div>
  );
};

export default Dashboard;
