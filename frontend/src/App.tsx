import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Layout from "./Layout/Layout";
import Error from "./components/Error";
import Dashboard from "./Page/Dashboard";
import Register from "./Page/Register";
import Login from "./Page/Login";
import CreateApp from "./Page/CreateApp";
import { scheduleTokenRefresh } from "./ultilities/tokenRefresh";
import { ProtectedRoute } from "./components/ProtectedRoutes";

scheduleTokenRefresh();

const router = createBrowserRouter([
  {
    element: <Layout />,
    errorElement: <Error />,

    children: [
      {
        path: "/",
        element: (
          <ProtectedRoute>
            {" "}
            <Dashboard />{" "}
          </ProtectedRoute>
        ),
      },

      {
        path: "/register",
        element: <Register />,
      },

      {
        path: "/login",
        element: <Login />,
      },

      {
        path: "/createApp",
        element: (
          <ProtectedRoute>
            {" "}
            <CreateApp />{" "}
          </ProtectedRoute>
        ),
      },
    ],
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
