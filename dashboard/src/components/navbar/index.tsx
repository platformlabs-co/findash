
import React from "react";
import { Link, useLocation } from "react-router-dom";
import routes from "routes";

const Navbar = (props: {
  brandText: string;
  secondary?: boolean | string;
}) => {
  const { brandText } = props;
  const location = useLocation();

  const activeRoute = (routePath: string) => {
    return location.pathname.includes(routePath);
  };

  return (
    <nav className="sticky top-0 z-40 flex w-full flex-row items-center justify-between bg-white/10 p-2 backdrop-blur-xl dark:bg-[#0b14374d]">
      <div className="flex items-center">
        <Link to="/admin/default" className="text-navy-700 dark:text-white text-xl font-bold">
          Dashboard
        </Link>
      </div>
      <div className="flex items-center space-x-4">
        {routes.map((route, index) => {
          if (route.layout === "/admin") {
            return (
              <Link
                key={index}
                to={route.layout + "/" + route.path}
                className={`flex items-center px-4 py-2 rounded-lg transition-colors ${
                  activeRoute(route.path)
                    ? "bg-brand-500 text-white"
                    : "text-navy-700 dark:text-white hover:bg-gray-100 dark:hover:bg-navy-700"
                }`}
              >
                <span className="mr-2">{route.icon}</span>
                <span>{route.name}</span>
              </Link>
            );
          }
          return null;
        })}
      </div>
    </nav>
  );
};

export default Navbar;
