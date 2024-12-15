
import MainDashboard from "views/admin/default";
import Vendors from "views/admin/vendors";
import Configuration from "views/admin/configuration";
import SignIn from "views/auth/SignIn";
import { MdHome, MdLock, MdSettings } from "react-icons/md";

const routes = [
  {
    name: "Dashboard",
    layout: "/admin",
    path: "default",
    icon: <MdHome className="h-6 w-6" />,
    component: <MainDashboard />,
  },
  {
    name: "Configuration",
    layout: "/admin", 
    path: "configuration",
    icon: <MdSettings className="h-6 w-6" />,
    component: <Configuration />,
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
