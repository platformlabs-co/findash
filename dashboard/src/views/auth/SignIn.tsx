
import { useAuth0 } from "@auth0/auth0-react";
import { MdDashboard, MdBarChart, MdAttachMoney } from "react-icons/md";

export default function SignIn() {
  const { loginWithRedirect } = useAuth0();

  return (
    <div className="mx-auto flex w-full max-w-[1200px] flex-col gap-8">
      {/* Header */}
      <div className="mt-16 text-center">
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
          description="Monitor your cloud spending across multiple vendors in real-time"
        />
        <FeatureCard 
          icon={<MdBarChart className="h-6 w-6"/>}
          title="Cost Analysis"
          description="Deep dive into spending patterns and identify optimization opportunities"
        />
        <FeatureCard 
          icon={<MdAttachMoney className="h-6 w-6"/>}
          title="Cost Forecasting"
          description="Predict future cloud costs using advanced analytics"
        />
      </div>

      {/* Sign In Button */}
      <div className="mx-auto w-full max-w-[400px] text-center">
        <button
          onClick={() => loginWithRedirect()}
          className="linear w-full rounded-xl bg-brand-500 py-3 text-base font-medium text-white transition duration-200 hover:bg-brand-600 active:bg-brand-700 dark:bg-brand-400 dark:text-white dark:hover:bg-brand-300 dark:active:bg-brand-200"
        >
          Sign In to Get Started
        </button>
        <p className="mt-4 text-sm text-gray-600 dark:text-gray-400">
          Free and open source. Start optimizing your cloud costs today.
        </p>
      </div>
    </div>
  );
}

const FeatureCard = ({ icon, title, description }) => (
  <div className="rounded-2xl border border-gray-200 bg-white p-6 dark:border-gray-700 dark:bg-navy-800">
    <div className="mb-4 inline-flex rounded-lg bg-brand-500 p-3 text-white dark:bg-brand-400">
      {icon}
    </div>
    <h3 className="mb-2 text-xl font-bold text-navy-700 dark:text-white">
      {title}
    </h3>
    <p className="text-base text-gray-600 dark:text-gray-400">
      {description}
    </p>
  </div>
);
