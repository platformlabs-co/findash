
import Card from "components/card";
import React, { useState, useEffect } from 'react';
import { useAuth0 } from "@auth0/auth0-react";
import { CallBackendService } from "utils";

const APIConfig = () => {
  const [configurations, setConfigurations] = useState<any[]>([]);
  const { getAccessTokenSilently } = useAuth0();

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchConfigs = async () => {
      try {
        const response = await CallBackendService(
          "/v1/users/me/api-configurations",
          getAccessTokenSilently
        );
        setConfigurations(response.data || []);
      } catch (error) {
        console.error("Failed to fetch API configurations:", error);
        setConfigurations([]);
      } finally {
        setLoading(false);
      }
    };
    fetchConfigs();
  }, [getAccessTokenSilently]);

  return (
    <Card extra="pb-6 p-[20px]">
      <div className="flex flex-col">
        <h2 className="text-lg font-bold text-navy-700 dark:text-white mb-4">
          API Configurations
        </h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left p-2">Type</th>
                <th className="text-left p-2">Status</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={2} className="p-2 text-center text-gray-500">
                    Loading configurations...
                  </td>
                </tr>
              ) : configurations.length > 0 ? (
                configurations.map((config, index) => (
                  <tr key={index} className="border-b border-gray-200">
                    <td className="p-2 capitalize">{config.type}</td>
                    <td className="p-2">
                      <span className="px-2 py-1 rounded-full bg-green-100 text-green-800">
                        Configured
                      </span>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={2} className="p-2 text-center text-gray-500">
                    No API configurations found
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </Card>
  );
};

export default APIConfig;
