import Card from "components/card";
import React, { useEffect, useState } from "react";
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
  const [activeTab, setActiveTab] = useState<"actual" | "forecast">("actual");
  const { getAccessTokenSilently } = useAuth0();

  const fetchForecastData = async () => {
    try {
      const response = await CallBackendService(
        `/v1/vendors-forecast/${props.vendorName}`,
        getAccessTokenSilently,
      );
      setForecastData(response);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching forecast data:", error);
      setError("Failed to load forecast data");
      setLoading(false);
    }
  };

  useEffect(() => {
    if (activeTab === "forecast") {
      fetchForecastData();
    }
  }, [activeTab]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await CallBackendService(
          `/v1/vendors-metrics/${props.vendorName.toLowerCase()}`,
          getAccessTokenSilently,
        );
        setMetrics(response);
        setError(null);
      } catch (error) {
        console.error(error);
        setError("Failed to fetch vendor metrics");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [props.vendorName, getAccessTokenSilently]);

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

  const getBarChartOptions = () => {
    if (!metrics?.data || !Array.isArray(metrics.data))
      return {
        chart: { toolbar: { show: false } },
        xaxis: { categories: [] },
        yaxis: { show: true },
      };
    return {
      chart: {
        toolbar: { show: false },
      },
      tooltip: {
        style: {
          fontSize: "12px",
          fontFamily: undefined,
          backgroundColor: "#000000",
        },
        theme: "dark",
      },
      xaxis: {
        categories: metrics.data.map((entry) => entry.month),
        show: true,
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
      <Card extra="pb-10 p-[20px]">
        <div className="flex h-64 items-center justify-center">
          <p>Loading metrics...</p>
        </div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card extra="pb-10 p-[20px]">
        <div className="flex h-64 items-center justify-center">
          <p className="text-red-500">{error}</p>
        </div>
      </Card>
    );
  }

  return (
    <Card extra="pb-10 p-[20px]">
      <div className="flex flex-col">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-xl font-bold text-navy-700 dark:text-white">
            {props.vendorName.toString().charAt(0).toUpperCase() +
              props.vendorName.toString().slice(1)}{" "}
            Monthly Costs
          </h2>
          <div className="flex space-x-2">
            <button
              onClick={() => setActiveTab("actual")}
              className={`rounded px-4 py-2 ${
                activeTab === "actual"
                  ? "bg-brand-500 text-white"
                  : "bg-gray-100 text-gray-600 dark:bg-navy-700 dark:text-gray-200"
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
                      `${process.env.REACT_APP_BACKEND_URL}/v1/vendors-forecast/${props.vendorName}?format=csv`,
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
                    a.download = `${props.vendorName}_forecast.csv`;
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
            {loading ? (
              <div className="flex h-64 items-center justify-center">
                <p className="text-gray-500">Loading cost data...</p>
              </div>
            ) : metrics?.data &&
              Array.isArray(metrics.data) &&
              metrics.data.length > 0 ? (
              <>
                <div className="h-[300px] w-full">
                  {metrics.data && Array.isArray(metrics.data) && (
                    <BarChart
                      chartData={getBarChartData()}
                      chartOptions={getBarChartOptions()}
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
              <p className="text-center text-gray-500">
                No cost data available
              </p>
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
                <p className="text-red-500">{error}</p>
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
                  <div className="rounded-xl bg-navy-700 p-4">
                    <p className="text-sm text-gray-400">Best Case Total</p>
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
                  <div className="rounded-xl bg-navy-700 p-4">
                    <p className="text-sm text-gray-400">
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
                  <div className="rounded-xl bg-navy-700 p-4">
                    <p className="text-sm text-gray-400">Worst Case Total</p>
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
