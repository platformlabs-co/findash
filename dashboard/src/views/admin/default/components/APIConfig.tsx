import Card from "components/card";
import React, { useState, useEffect } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { CallBackendService } from "utils";
import DatadogConfig from "./DatadogConfig";

const APIConfig = () => {
  const [configurations, setConfigurations] = useState<any[]>([]);
  const [showDatadogConfig, setShowDatadogConfig] = useState(false);
  const { getAccessTokenSilently } = useAuth0();
  const [loading, setLoading] = useState(true);

  const fetchConfigs = async () => {
    try {
      const response = await CallBackendService(
        "/v1/users/me/api-configurations",
        getAccessTokenSilently,
      );
      setConfigurations(response.data || []);
      // Hide DatadogConfig if we have a configuration
      setShowDatadogConfig(
        !response.data?.some((config: any) => config.type === "datadog"),
      );
    } catch (error) {
      console.error("Failed to fetch API configurations:", error);
      setConfigurations([]);
      setShowDatadogConfig(true);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchConfigs();
  }, [getAccessTokenSilently]);

  return (
    <>
      <Card extra="pb-6 p-[20px]">
        <div className="flex flex-col">
          <h2 className="mb-4 text-lg font-bold text-navy-700 dark:text-white">
            API Configurations
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="p-2 text-left">Type</th>
                  <th className="p-2 text-left">Status</th>
                  <th className="p-2 text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr>
                    <td colSpan={3} className="p-2 text-center text-gray-500">
                      Loading configurations...
                    </td>
                  </tr>
                ) : configurations.length > 0 ? (
                  configurations.map((config, index) => (
                    <tr key={index} className="border-b border-gray-200">
                      <td className="p-2 capitalize">{config.type}</td>
                      <td className="p-2">
                        <span className="rounded-full bg-green-100 px-2 py-1 text-green-800">
                          Configured
                        </span>
                      </td>
                      <td className="p-2 text-right">
                        <button
                          onClick={() => setShowDatadogConfig(true)}
                          className="rounded bg-brand-500 px-3 py-1 text-sm text-white hover:bg-brand-600"
                        >
                          Change Configuration
                        </button>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={3} className="p-2 text-center text-gray-500">
                      No API configurations found
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </Card>
      {showDatadogConfig && (
        <div className="mt-4">
          <DatadogConfig
            onSave={() => {
              setShowDatadogConfig(false);
              fetchConfigs();
            }}
          />
        </div>
      )}
    </>
  );
};

export default APIConfig;
