
import Card from "components/card";
import React, { useState } from 'react';
import { useAuth0 } from "@auth0/auth0-react";
import { CallBackendService } from "utils";

const DatadogConfig = () => {
  const [appKey, setAppKey] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [message, setMessage] = useState('');
  const { getAccessTokenSilently } = useAuth0();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await CallBackendService(
        "/v1/users/me/datadog-configuration",
        getAccessTokenSilently,
        {
          method: 'POST',
          body: JSON.stringify({ app_key: appKey, api_key: apiKey }),
          headers: { 'Content-Type': 'application/json' }
        }
      );
      setMessage('Configuration saved successfully!');
      setAppKey('');
      setApiKey('');
    } catch (error) {
      setMessage('Failed to save configuration');
      console.error(error);
    }
  };

  return (
    <Card extra="pb-6 p-[20px]">
      <div className="flex flex-col">
        <h2 className="text-lg font-bold text-navy-700 dark:text-white mb-4">
          Datadog Configuration
        </h2>
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            type="text"
            value={appKey}
            onChange={(e) => setAppKey(e.target.value)}
            placeholder="App Key"
            className="px-3 py-2 border rounded text-gray-800"
          />
          <input
            type="text"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="API Key"
            className="px-3 py-2 border rounded text-gray-800"
          />
          <button
            type="submit"
            className="bg-brand-500 text-white px-4 py-2 rounded"
          >
            Save Configuration
          </button>
        </form>
        {message && (
          <p className="mt-4 text-center">{message}</p>
        )}
      </div>
    </Card>
  );
};

export default DatadogConfig;
