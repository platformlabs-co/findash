// Admin Imports
import MainDashboard from "views/admin/default";
import Vendors from "views/admin/vendors";
import SignIn from "views/auth/SignIn";

// Auth Imports

// Icon Imports
import {
  MdHome, MdLock
} from "react-icons/md";

const routes = [
  {
    name: "Dashboard",
    layout: "/admin",
    path: "default",
    icon: <MdHome className="h-6 w-6" />,
    component: <MainDashboard />,
  },
  {
    name: "Vendors",
    layout: "/admin",
    path: "vendors",
    icon: <MdHome className="h-6 w-6" />,
    component: <Vendors />,
  },
  {
    name: "Sign In",
    layout: "/auth",
    path: "sign-in",
    icon: <MdLock className="h-6 w-6" />,
    component: <SignIn />,
  },
];
export default routes;
