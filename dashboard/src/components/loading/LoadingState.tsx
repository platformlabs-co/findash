
import React from 'react';

export const LoadingState = () => {
  return (
    <div className="flex h-screen w-full items-center justify-center bg-navy-900">
      <div className="flex flex-col items-center">
        <div className="h-12 w-12 animate-spin rounded-full border-4 border-solid border-brand-500 border-t-transparent"></div>
        <p className="mt-4 text-lg font-medium text-white">Loading your dashboard...</p>
      </div>
    </div>
  );
};
