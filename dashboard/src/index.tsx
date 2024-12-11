import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { Auth0Provider } from '@auth0/auth0-react';
import "./index.css";
import App from "./App";

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <Auth0Provider
      domain="platformlabs.us.auth0.com"
      clientId="mlUVKKqaYLc0QBITyOXT1ev0a1D5v72l"
      authorizationParams={{
        redirect_uri: window.location.origin
      }}
    >
  <BrowserRouter>
    <App />
  </BrowserRouter>
  </Auth0Provider>
);
