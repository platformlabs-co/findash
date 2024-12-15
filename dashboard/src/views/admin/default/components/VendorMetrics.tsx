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
  const [forecastData, setForecastData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [activeTab, setActiveTab] = useState<'actual' | 'forecast'>('actual');
  const { getAccessTokenSilently } = useAuth0();

  const fetchForecastData = async () => {
    try {
      const response = await CallBackendService(
        `/v1/vendors-forecast/${props.vendorName}`,
        getAccessTokenSilently
      );
      setForecastData(response);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching forecast data:', error);
      setError('Failed to load forecast data');
      setLoading(false);
    }
  };

  useEffect(() => {
    if (activeTab === 'forecast') {
      fetchForecastData();
    }
  }, [activeTab]);

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
    if (!metrics?.data) return [{ name: "Monthly Cost", data: [], color: "#4318FF" }];
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
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold text-navy-700 dark:text-white">
            {props.vendorName.toString().charAt(0).toUpperCase() + props.vendorName.toString().slice(1)} Monthly Costs
          </h2>
          <div className="flex space-x-2">
            <button
              onClick={() => setActiveTab('actual')}
              className={`px-4 py-2 rounded ${
                activeTab === 'actual'
                  ? 'bg-brand-500 text-white'
                  : 'bg-gray-100 text-gray-600 dark:bg-navy-700 dark:text-gray-200'
              }`}
            >
              Actual
            </button>
            <button
              onClick={() => setActiveTab('forecast')}
              className={`px-4 py-2 rounded ${
                activeTab === 'forecast'
                  ? 'bg-brand-500 text-white'
                  : 'bg-gray-100 text-gray-600 dark:bg-navy-700 dark:text-gray-200'
              }`}
            >
              Forecast
            </button>
          </div>
        </div>
        
        {activeTab === 'actual' && metrics?.data && metrics.data.length > 0 ? (
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
        
        {activeTab === 'forecast' && (
          <>
            {loading ? (
              <div className="flex items-center justify-center h-64">
                <p className="text-gray-500">Loading forecast data...</p>
              </div>
            ) : error ? (
              <div className="flex items-center justify-center h-64">
                <p className="text-red-500">{error}</p>
              </div>
            ) : forecastData?.data && forecastData.data.length > 0 ? (
              <div className="h-[300px] w-full">
                <BarChart
                  chartData={[
                    {
                      name: "Forecast",
                      data: forecastData.data.map((item: any) => item.predicted_cost)
                    }
                  ]}
                  chartOptions={{
                    xaxis: {
                      categories: forecastData.data.map((item: any) => item.month),
                      labels: {
                        style: {
                          colors: "#A3AED0",
                          fontSize: "12px",
                          fontWeight: "500",
                        },
                      },
                    },
                  }}
                />
              </div>
            ) : (
              <div className="flex items-center justify-center h-64">
                <p className="text-gray-500">No forecast data available</p>
              </div>
            )}
          </>
        )}
      </div>
    </Card>
  );
};

export default VendorMetrics;