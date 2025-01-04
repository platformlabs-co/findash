import MainDashboard from "views/admin/default";
import Vendors from "views/admin/vendors";
import Configuration from "views/admin/configuration";
import SignIn from "views/auth/SignIn";
import { MdHome, MdLock, MdSettings, MdHelp } from "react-icons/md";
import Support from "views/admin/support";

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
  {
    name: "Support",
    layout: "/auth",
    path: "support",
    icon: <MdHelp className="h-6 w-6" />,
    component: <Support />,
  },
];
export default routes;
