import Card from "components/card";
import React, { useState, useEffect } from 'react';
import { useAuth0 } from "@auth0/auth0-react";
import { CallBackendService } from "utils";

interface DatadogConfigProps {
  onConfigured?: () => void;
  existingConfig?: boolean;
}

const DatadogConfig: React.FC<DatadogConfigProps> = ({ onConfigured, existingConfig }) => {
  const [appKey, setAppKey] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const { getAccessTokenSilently } = useAuth0();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      await CallBackendService(
        "/v1/configuration/datadog",
        getAccessTokenSilently,
        {
          method: 'POST',
          body: JSON.stringify({ app_key: appKey, api_key: apiKey }),
          headers: { 'Content-Type': 'application/json' }
        }
      );

      setSuccess(existingConfig 
        ? "Datadog credentials updated successfully!" 
        : "Datadog credentials configured successfully!");
      setAppKey('');
      setApiKey('');
      
      if (onConfigured) {
        onConfigured();
      }
    } catch (error: any) {
      setError(error.message || "Failed to configure Datadog credentials");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card extra="!p-[20px] text-center">
      <div className="relative flex flex-row justify-between">
        <div className="flex items-center">
          <div className="flex h-9 w-9 items-center justify-center rounded-full bg-indigo-100 dark:bg-indigo-100 dark:bg-white/5">
            <svg
              className="h-6 w-6 text-brand-500 dark:text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
              />
            </svg>
          </div>
          <h5 className="ml-4 text-lg font-bold text-navy-700 dark:text-white">
            Datadog Configuration
          </h5>
        </div>
      </div>

      <div className="mt-8 w-full">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="flex flex-col">
            <label className="mb-2 text-sm font-medium text-gray-900 dark:text-white">
              Datadog App Key {existingConfig && "(leave blank to keep current)"}
            </label>
            <input
              type="password"
              value={appKey}
              onChange={(e) => setAppKey(e.target.value)}
              className="mt-2 flex h-12 w-full items-center justify-center rounded-xl border bg-white/0 p-3 text-sm outline-none border-gray-200 dark:!border-white/10 dark:text-white"
              placeholder={existingConfig ? "Enter new Datadog App Key" : "Enter Datadog App Key"}
              required={!existingConfig}
            />
          </div>

          <div className="flex flex-col">
            <label className="mb-2 text-sm font-medium text-gray-900 dark:text-white">
              Datadog API Key {existingConfig && "(leave blank to keep current)"}
            </label>
            <input
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              className="mt-2 flex h-12 w-full items-center justify-center rounded-xl border bg-white/0 p-3 text-sm outline-none border-gray-200 dark:!border-white/10 dark:text-white"
              placeholder={existingConfig ? "Enter new Datadog API Key" : "Enter Datadog API Key"}
              required={!existingConfig}
            />
          </div>

          {error && (
            <div className="mt-4 rounded-lg bg-red-50 p-4 text-sm text-red-500 dark:bg-red-900/20">
              {error}
            </div>
          )}

          {success && (
            <div className="mt-4 rounded-lg bg-green-50 p-4 text-sm text-green-500 dark:bg-green-900/20">
              {success}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className={`linear mt-4 w-full rounded-xl bg-brand-500 px-4 py-3 text-base font-medium text-white transition duration-200 hover:bg-brand-600 active:bg-brand-700 dark:bg-brand-400 dark:text-white dark:hover:bg-brand-300 dark:active:bg-brand-200 ${
              loading ? "cursor-not-allowed opacity-50" : ""
            }`}
          >
            {loading ? "Configuring..." : (existingConfig ? "Update Datadog" : "Configure Datadog")}
          </button>
        </form>
      </div>
    </Card>
  );
};

export default DatadogConfig;
