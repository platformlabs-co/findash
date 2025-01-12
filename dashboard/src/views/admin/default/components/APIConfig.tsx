import Card from "components/card";
import React, { useState } from "react";
import { useAPIConfigurations } from "./hooks/useAPIConfigurations";
import Modal from "components/modal";
import DatadogConfig from "./DatadogConfig";
import AWSConfig from "./AWSConfig";

interface VendorConfig {
  id: string;
  name: string;
  type: string;
  component: React.ComponentType<any>;
}

const VENDOR_CONFIGS: VendorConfig[] = [
  {
    id: "datadog",
    name: "Datadog",
    type: "datadog",
    component: DatadogConfig,
  },
  {
    id: "aws",
    name: "AWS",
    type: "aws",
    component: AWSConfig,
  },
];

const APIConfig = () => {
  const { configurations, loading, error, refresh } = useAPIConfigurations();
  const [showConfigModal, setShowConfigModal] = useState(false);
  const [selectedVendor, setSelectedVendor] = useState<VendorConfig | null>(null);

  const handleConfigureVendor = (vendor: VendorConfig) => {
    setSelectedVendor(vendor);
    setShowConfigModal(true);
  };

  const handleCloseModal = () => {
    setShowConfigModal(false);
    setSelectedVendor(null);
  };

  const isVendorConfigured = (vendorType: string) => {
    return configurations.some((config) => config.type === vendorType);
  };

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
                  <th className="p-2 text-left">Vendor</th>
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
                ) : (
                  VENDOR_CONFIGS.map((vendor) => {
                    const configured = isVendorConfigured(vendor.type);
                    return (
                      <tr key={vendor.id} className="border-b border-gray-200">
                        <td className="p-2 capitalize">{vendor.name}</td>
                        <td className="p-2">
                          <span
                            className={`rounded-full px-2 py-1 text-sm ${
                              configured
                                ? "bg-green-100 text-green-800"
                                : "bg-gray-100 text-gray-800"
                            }`}
                          >
                            {configured ? "Configured" : "Not Configured"}
                          </span>
                        </td>
                        <td className="p-2 text-right">
                          <button
                            onClick={() => handleConfigureVendor(vendor)}
                            className="rounded bg-brand-500 px-3 py-1 text-sm text-white hover:bg-brand-600"
                          >
                            {configured
                              ? "Change Configuration"
                              : "Add Configuration"}
                          </button>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>
      </Card>

      {showConfigModal && selectedVendor && (
        <Modal
          isOpen={showConfigModal}
          onClose={handleCloseModal}
          title={`${
            isVendorConfigured(selectedVendor.type) ? "Update" : "Add"
          } ${selectedVendor.name} Configuration`}
        >
          {React.createElement(selectedVendor.component, {
            onConfigured: () => {
              refresh();
              handleCloseModal();
            },
            existingConfig: isVendorConfigured(selectedVendor.type),
          })}
        </Modal>
      )}
    </>
  );
};

export default APIConfig;
