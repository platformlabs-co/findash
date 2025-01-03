import Card from "components/card";
import React, { useEffect, useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { CallBackendService } from "utils";
import BarChart from "components/charts/BarChart";
import { ApexOptions } from "apexcharts";
import { DatadogIcon, AWSIcon } from "../../../../components/icons";

interface MonthlyMetric {
  month: string;
  cost: number;
}

interface VendorMetricsData {
  data: MonthlyMetric[];
  message?: string;
}

interface APIError {
  message: string;
  isConnectionError: boolean;
}

interface VendorMetricsProps {
  vendor: "datadog" | "aws";
  title: string;
}

const VendorMetrics: React.FC<VendorMetricsProps> = ({ vendor, title }) => {
  const [metrics, setMetrics] = useState<VendorMetricsData | null>(null);
  const [forecastData, setForecastData] = useState<any>(null);
  const [error, setError] = useState<APIError | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [activeTab, setActiveTab] = useState<"actual" | "forecast">("actual");
  const { getAccessTokenSilently } = useAuth0();

  const fetchForecastData = async () => {
    try {
      const response = await CallBackendService(
        `/v1/vendors-forecast/${vendor}`,
        getAccessTokenSilently,
      );
      setForecastData(response);
      setError(null);
    } catch (error: any) {
      console.error("Error fetching forecast data:", error);
      setError({
        message: "Failed to load forecast data",
        isConnectionError: error.message?.includes('Failed to fetch') || !error.response
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (activeTab === "forecast") {
      fetchForecastData();
    }
  }, [activeTab]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const response = await CallBackendService(
        `/v1/vendors-metrics/${vendor.toLowerCase()}`,
        getAccessTokenSilently,
      );
      setMetrics(response);
      setError(null);
    } catch (error: any) {
      console.error(error);
      setError({
        message: error.message || "Failed to fetch vendor metrics",
        isConnectionError: error.message?.includes('Failed to fetch') || !error.response
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [vendor, getAccessTokenSilently]);

  const getBarChartData = () => {
    if (!metrics?.data || !Array.isArray(metrics.data))
      return [{ name: "Monthly Cost", data: [], color: "#4318FF" }];
    return [
      {
        name: "Monthly Cost",
        data: metrics.data.map((entry) => entry.cost),
        color: "#4318FF",
      },
    ];
  };

  const getChartOptions = (chartData: any): ApexOptions => {
    if (!chartData)
      return {
        chart: { toolbar: { show: false } },
        xaxis: { categories: [] as string[] },
        yaxis: { show: true },
      };
    return {
      chart: {
        toolbar: {
          show: false,
        },
      },
      tooltip: {
        style: {
          fontSize: "12px",
          fontFamily: undefined as unknown as string,
        },
        theme: "dark",
      },
      xaxis: {
        categories: chartData.map((entry: any) => entry.month),
        labels: {
          show: true,
          style: {
            colors: "#A3AED0",
            fontSize: "14px",
            fontWeight: "500",
          },
        },
      },
      yaxis: {
        show: true,
        labels: {
          show: true,
          style: {
            colors: "#A3AED0",
            fontSize: "14px",
            fontWeight: "500",
          },
          formatter: function (value: number) {
            return "$" + value.toFixed(2);
          },
        },
      },
      fill: {
        type: "solid",
        colors: ["#4318FF"],
      },
      dataLabels: {
        enabled: false,
      },
      plotOptions: {
        bar: {
          borderRadius: 3,
          columnWidth: "40px",
        },
      },
    };
  };

  if (loading) {
    return (
      <Card extra="pb-10 p-[20px] bg-white dark:!bg-gray-800">
        <div className="flex h-64 items-center justify-center">
          <div className="text-center">
            <div className="mb-4 h-8 w-8 animate-spin rounded-full border-4 border-solid border-brand-500 border-t-transparent mx-auto"></div>
            <p className="text-gray-600 dark:text-gray-400">Loading metrics...</p>
          </div>
        </div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card extra="pb-10 p-[20px] bg-white dark:!bg-gray-800">
        <div className="flex h-64 items-center justify-center">
          <div className="text-center">
            {error.isConnectionError ? (
              <>
                <div className="mb-4">
                  <svg className="h-12 w-12 mx-auto text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                </div>
                <p className="text-red-500 font-medium mb-2">API Connection Error</p>
                <p className="text-gray-600 dark:text-gray-400 text-sm">
                  Unable to connect to the API server. Please check your connection or try again later.
                </p>
                <button
                  onClick={() => {
                    setError(null);
                    setLoading(true);
                    fetchData();
                  }}
                  className="mt-4 px-4 py-2 bg-brand-500 text-white rounded-lg hover:bg-brand-600 transition-colors"
                >
                  Retry Connection
                </button>
              </>
            ) : (
              <p className="text-red-500">{error.message}</p>
            )}
          </div>
        </div>
      </Card>
    );
  }

  return (
    <Card extra="!p-[20px] text-center bg-white dark:!bg-gray-800">
      <div className="relative flex flex-row justify-between">
        <div className="flex items-center">
          <div className="flex h-9 w-9 items-center justify-center rounded-full bg-gray-100 dark:bg-navy-700">
            {vendor === "datadog" ? (
              <DatadogIcon className="h-6 w-6 text-brand-500 dark:text-white" />
            ) : (
              <AWSIcon className="h-6 w-6 text-brand-500 dark:text-white" />
            )}
          </div>
          <h5 className="ml-4 text-lg font-bold text-gray-700 dark:text-white">
            {title}
          </h5>
        </div>
      </div>
      <div className="flex flex-col">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-700 dark:text-white">
            {vendor.toString().charAt(0).toUpperCase() +
              vendor.toString().slice(1)}{" "}
            Monthly Costs
          </h2>
          <div className="flex space-x-2">
            <button
              onClick={() => setActiveTab("actual")}
              className={`rounded px-4 py-2 ${
                activeTab === "actual"
                  ? "bg-brand-500 text-white"
                  : "bg-gray-100 text-gray-600 dark:bg-navy-700 dark:text-navy-200"
              }`}
            >
              Actual
            </button>
            <button
              onClick={() => setActiveTab("forecast")}
              className={`rounded px-4 py-2 ${
                activeTab === "forecast"
                  ? "bg-brand-500 text-white"
                  : "bg-gray-100 text-gray-600 dark:bg-navy-700 dark:text-gray-200"
              }`}
            >
              Forecast
            </button>
            {activeTab === "forecast" && (
              <button
                onClick={async () => {
                  try {
                    const token = await getAccessTokenSilently();
                    const response = await fetch(
                      `${process.env.REACT_APP_BACKEND_URL}/v1/vendors-forecast/${vendor}?format=csv`,
                      {
                        headers: {
                          Authorization: `Bearer ${token}`,
                        },
                      }
                    );
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `${vendor}_forecast.csv`;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                  } catch (error) {
                    console.error("Export failed:", error);
                  }
                }}
                className="rounded bg-green-500 px-4 py-2 text-white hover:bg-green-600"
              >
                Export CSV
              </button>
            )}
          </div>
        </div>

        {activeTab === "actual" && (
          <>
            {error ? (
              <div className="flex h-64 items-center justify-center">
                <p className="text-red-500">{error.message}</p>
              </div>
            ) : loading ? (
              <div className="flex h-64 items-center justify-center">
                <p className="text-gray-500">Loading data...</p>
              </div>
            ) : metrics?.data && metrics.data.length > 0 ? (
              <>
                <div className="h-[300px] w-full">
                  {metrics.data && Array.isArray(metrics.data) && (
                    <BarChart
                      chartData={getBarChartData()}
                      chartOptions={getChartOptions(metrics.data)}
                    />
                  )}
                </div>
                <div className="mt-6 overflow-x-auto">
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
                          <td className="py-3 text-right">
                            $
                            {entry.cost.toLocaleString("en-US", {
                              minimumFractionDigits: 2,
                              maximumFractionDigits: 2,
                            })}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </>
            ) : (
              <div className="flex h-64 items-center justify-center">
                <p className="text-center text-gray-500">
                  No API configuration found for {vendor.toString()}
                </p>
              </div>
            )}
          </>
        )}

        {activeTab === "forecast" && (
          <>
            {loading ? (
              <div className="flex h-64 items-center justify-center">
                <p className="text-gray-500">Loading forecast data...</p>
              </div>
            ) : error ? (
              <div className="flex h-64 items-center justify-center">
                <p className="text-red-500">{error.message}</p>
              </div>
            ) : loading ? (
              <div className="flex h-64 items-center justify-center">
                <p className="text-gray-500">Loading forecast data...</p>
              </div>
            ) : forecastData?.forecast &&
              Array.isArray(forecastData.forecast) &&
              forecastData.forecast.length > 0 ? (
              <>
                <div className="mb-6 grid grid-cols-3 gap-4">
                  <div className="rounded-xl dark:bg-navy-900 p-4">
                    <p className="text-sm text-gray-700 dark:text-gray-400">Best Case Total</p>
                    <p className="text-xl text-green-500">
                      $
                      {forecastData.sums.total_best_case.toLocaleString(
                        "en-US",
                        { minimumFractionDigits: 2, maximumFractionDigits: 2 },
                      )}
                      <span className="mt-1 block text-sm text-gray-400">
                        MoM Growth: {forecastData.growth_rates.best_case}%
                      </span>
                    </p>
                  </div>
                  <div className="rounded-xl dark:bg-navy-900 p-4">
                    <p className="text-sm text-gray-700 dark:text-gray-400">
                      Trend-based Forecast Total
                    </p>
                    <p className="text-xl text-white">
                      $
                      {forecastData.sums.total_forecast.toLocaleString(
                        "en-US",
                        { minimumFractionDigits: 2, maximumFractionDigits: 2 },
                      )}
                      <span className="mt-1 block text-sm text-gray-400">
                        MoM Growth: {forecastData.growth_rates.trend_based}%
                      </span>
                    </p>
                  </div>
                  <div className="rounded-xl dark:bg-navy-900 p-4">
                    <p className="text-sm text-gray-700 dark:text-gray-400">Worst Case Total</p>
                    <p className="text-xl text-red-500">
                      $
                      {forecastData.sums.total_worst_case.toLocaleString(
                        "en-US",
                        { minimumFractionDigits: 2, maximumFractionDigits: 2 },
                      )}
                      <span className="mt-1 block text-sm text-gray-400">
                        MoM Growth: {forecastData.growth_rates.worst_case}%
                      </span>
                    </p>
                  </div>
                </div>
                <div className="mt-6 overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-gray-200">
                        <th className="py-3 text-left">Month</th>
                        <th className="py-3 text-right">Best Case</th>
                        <th className="py-3 text-right">
                          Trend-based Forecast
                        </th>
                        <th className="py-3 text-right">Worst Case</th>
                      </tr>
                    </thead>
                    <tbody>
                      {forecastData.forecast.map(
                        (entry: any, index: number) => (
                          <tr key={index} className="border-b border-gray-200">
                            <td className="py-3">{entry.month}</td>
                            <td className="py-3 text-right text-green-500">
                              $
                              {entry.best_case.toLocaleString("en-US", {
                                minimumFractionDigits: 2,
                                maximumFractionDigits: 2,
                              })}
                            </td>
                            <td className="py-3 text-right">
                              $
                              {entry.cost.toLocaleString("en-US", {
                                minimumFractionDigits: 2,
                                maximumFractionDigits: 2,
                              })}
                            </td>
                            <td className="py-3 text-right text-red-500">
                              $
                              {entry.worst_case.toLocaleString("en-US", {
                                minimumFractionDigits: 2,
                                maximumFractionDigits: 2,
                              })}
                            </td>
                          </tr>
                        ),
                      )}
                    </tbody>
                  </table>
                </div>
              </>
            ) : (
              <div className="flex h-64 items-center justify-center">
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
