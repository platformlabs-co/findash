import { useEffect } from "react";
import APIConfig from "../default/components/APIConfig";

export default function Configuration() {
  useEffect(() => {
    document.title = "Configuration";
  }, []);

  return (
    <div className="mt-3">
      <div className="mb-4">
        <h1 className="text-2xl font-bold text-navy-700 dark:text-white">
          Configuration
        </h1>
      </div>
      <div className="mt-5 grid grid-cols-1 gap-5">
        <APIConfig />
      </div>
    </div>
  );
}
