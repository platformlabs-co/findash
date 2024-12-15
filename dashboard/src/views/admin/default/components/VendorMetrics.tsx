
import Card from "components/card";
import React, { useEffect, useState } from 'react';
import { useAuth0 } from "@auth0/auth0-react";
import { CallBackendService } from "utils";

interface DatadogCost {
  data: {
    attributes: {
      date: string;
      total_cost: number;
    }[];
  };
  message: string;
}

const VendorMetrics = (props: { vendorName: String }) => {
  const [metrics, setMetrics] = useState<DatadogCost | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const { getAccessTokenSilently } = useAuth0();

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await CallBackendService(
          `/v1/vendors-metrics/${props.vendorName.toLowerCase()}`,
          getAccessTokenSilently
        );
        setMetrics(response);
        setError(null);
      } catch (error) {
        console.error(error);
        setError('Failed to fetch vendor metrics');
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [props.vendorName]);

  if (loading) {
    return (
      <Card extra="pb-10 p-[20px]">
        <div className="flex items-center justify-center h-64">
          <p>Loading metrics...</p>
        </div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card extra="pb-10 p-[20px]">
        <div className="flex items-center justify-center h-64">
          <p className="text-red-500">{error}</p>
        </div>
      </Card>
    );
  }

  return (
    <Card extra="pb-10 p-[20px]">
      <div className="flex flex-col">
        <h2 className="text-xl font-bold mb-4 text-navy-700 dark:text-white">
          {props.vendorName} Cost Metrics
        </h2>
        
        {metrics?.data?.attributes ? (
          <div className="space-y-4">
            <div className="bg-navy-700 dark:bg-navy-800 rounded-lg p-4">
              <h3 className="text-lg text-white mb-2">Latest Cost</h3>
              <p className="text-3xl font-bold text-white">
                ${metrics.data.attributes[metrics.data.attributes.length - 1]?.total_cost.toFixed(2)}
              </p>
            </div>
            
            <div className="bg-white dark:bg-navy-800 rounded-lg p-4">
              <h3 className="text-lg mb-2">Cost History</h3>
              <div className="max-h-64 overflow-y-auto">
                {metrics.data.attributes.map((entry, index) => (
                  <div 
                    key={index}
                    className="flex justify-between py-2 border-b border-gray-200 dark:border-navy-700"
                  >
                    <span>{new Date(entry.date).toLocaleDateString()}</span>
                    <span className="font-semibold">${entry.total_cost.toFixed(2)}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <p className="text-center text-gray-500">No cost data available</p>
        )}
      </div>
    </Card>
  );
};

export default VendorMetrics;
