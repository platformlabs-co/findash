import React from "react";
import { Link } from "react-router-dom";
import { useAuth0 } from "@auth0/auth0-react";
import { MdDashboard, MdBarChart, MdAttachMoney } from "react-icons/md";
import logoWhite from "assets/img/layout/logoWhite.png";

export default function SignIn() {
  const { loginWithRedirect } = useAuth0();

  return (
    <div className="mx-auto flex w-full max-w-[1200px] flex-col gap-8">
      {/* Header */}
      <div className="mt-16 text-center">
        <img src={logoWhite} alt="FinDash Logo" className="mx-auto mb-6 h-44" />
        <h1 className="mb-2 text-4xl font-bold text-navy-700 dark:text-white">
          FinDash - Open Source FinOps Dashboard
        </h1>
        <p className="mb-8 text-xl text-gray-600 dark:text-gray-400">
          Explore, analyze and optimize your cloud spending
        </p>
      </div>

      {/* Features Grid */}
      <div className="mb-8 grid grid-cols-1 gap-6 md:grid-cols-3">
        <FeatureCard 
          icon={<MdDashboard className="h-6 w-6"/>}
          title="Budget Tracking"
          description="Monitor your cloud spending across multiple vendors"
        />
        <FeatureCard 
          icon={<MdAttachMoney className="h-6 w-6"/>}
          title="Cost Forecasting"
          description="Predict future cloud costs using common forecasting techniques"
        />
        <FeatureCard 
          icon={<MdBarChart className="h-6 w-6"/>}
          title="AI-Powered Insights"
          description="We use AI to provide accurate forecasts and optimization suggestions"
          soon
        />
      </div>

      {/* Sign In Button and Support Link */}
      <div className="mx-auto w-full max-w-[400px] text-center">
        <button
          onClick={() => loginWithRedirect()}
          className="linear w-full rounded-xl bg-brand-500 py-3 text-base font-medium text-white transition duration-200 hover:bg-brand-600 active:bg-brand-700 dark:bg-brand-400 dark:text-white dark:hover:bg-brand-300 dark:active:bg-brand-200"
        >
          Sign In to Get Started
        </button>
        <div className="mt-4 flex flex-col items-center justify-center gap-2">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Free and open source. Start optimizing your cloud costs today.
          </p>
          <Link
            to="/auth/support"
            className="text-sm font-medium text-brand-500 hover:text-brand-600 dark:text-white"
          >
            Find more about us →
          </Link>
        </div>
      </div>
    </div>
  );
}

const FeatureCard = ({ 
  icon, 
  title, 
  description, 
  soon 
}: { 
  icon: React.ReactNode; 
  title: string; 
  description: string;
  soon?: boolean;
}) => (
  <div className="rounded-2xl border border-gray-200 bg-white p-6 dark:border-gray-700 dark:bg-navy-800">
    <div className="mb-4 flex items-center gap-2">
      <div className="inline-flex rounded-lg bg-brand-500 p-3 text-white dark:bg-brand-400">
        {icon}
      </div>
      {soon && (
        <span className="rounded-full bg-indigo-100 px-3 py-1 text-xs font-semibold text-indigo-500">
          SOON
        </span>
      )}
    </div>
    <h3 className="mb-2 text-xl font-bold text-navy-700 dark:text-white">
      {title}
    </h3>
    <p className="text-base text-gray-600 dark:text-gray-400">
      {description}
    </p>
  </div>
);
