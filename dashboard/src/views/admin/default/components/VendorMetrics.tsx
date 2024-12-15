
import Card from "components/card";
import React, { useEffect, useState } from 'react';
import { useAuth0 } from "@auth0/auth0-react";
import { CallBackendService } from "utils";
import BarChart from "components/charts/BarChart";

interface MonthlyMetric {
  month: string;
  cost: number;
}

interface VendorMetricsData {
  data: MonthlyMetric[];
  message?: string;
}

const VendorMetrics = (props: { vendorName: String }) => {
  const [metrics, setMetrics] = useState<VendorMetricsData | null>(null);
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
  }, [props.vendorName, getAccessTokenSilently]);

  const getBarChartData = () => {
    if (!metrics?.data) return [];
    return [{
      name: "Monthly Cost",
      data: metrics.data.map(entry => entry.cost),
      color: "#4318FF"
    }];
  };

  const getBarChartOptions = () => {
    if (!metrics?.data) return {};
    return {
      chart: {
        toolbar: { show: false },
      },
      tooltip: {
        style: {
          fontSize: "12px",
          fontFamily: undefined,
          backgroundColor: "#000000"
        },
        theme: "dark"
      },
      xaxis: {
        categories: metrics.data.map(entry => entry.month),
        show: true,
        labels: {
          show: true,
          style: {
            colors: "#A3AED0",
            fontSize: "14px",
            fontWeight: "500"
          }
        }
      },
      yaxis: {
        show: true,
        labels: {
          show: true,
          style: {
            colors: "#A3AED0",
            fontSize: "14px",
            fontWeight: "500"
          },
          formatter: function (value: number) {
            return "$" + value.toFixed(2);
          }
        }
      },
      fill: {
        type: "solid",
        colors: ["#4318FF"]
      },
      dataLabels: {
        enabled: false
      },
      plotOptions: {
        bar: {
          borderRadius: 3,
          columnWidth: "40px"
        }
      }
    };
  };

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
          {props.vendorName.toString().charAt(0).toUpperCase() + props.vendorName.toString().slice(1)} Monthly Costs
        </h2>
        
        {metrics?.data && metrics.data.length > 0 ? (
          <>
            <div className="h-[300px] w-full">
              <BarChart
                chartData={getBarChartData()}
                chartOptions={getBarChartOptions()}
              />
            </div>
            <div className="overflow-x-auto mt-6">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="py-3 text-left">Month</th>
                    <th className="py-3 text-right">Cost</th>
                  </tr>
                </thead>
                <tbody>
                  {metrics.data.map((entry, index) => (
                    <tr key={index} className="border-b border-gray-200">
                      <td className="py-3">{entry.month}</td>
                      <td className="py-3 text-right">${entry.cost.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        ) : (
          <p className="text-center text-gray-500">No cost data available</p>
        )}
      </div>
    </Card>
  );
};

export default VendorMetrics;
