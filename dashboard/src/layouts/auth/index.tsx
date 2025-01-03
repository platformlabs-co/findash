import React from "react";
import { Routes, Route } from "react-router-dom";
import routes from "routes";

export default function Auth() {
  return (
    <div className="relative h-full w-full bg-navy-900">
      <main className="mx-auto h-full min-h-screen">
        <div className="relative flex h-full">
          <div className="mx-auto flex min-h-full w-full flex-col justify-start pt-12 md:max-w-[75%]">
            <Routes>
              {routes.map((route, key) => {
                if (route.layout === "/auth") {
                  return (
                    <Route
                      path={`/${route.path}`}
                      element={route.component}
                      key={key}
                    />
                  );
                }
                return null;
              })}
            </Routes>
          </div>
        </div>
      </main>
    </div>
  );
}
