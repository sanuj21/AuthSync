import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Layout from "./Layout/Layout";
import Error from "./components/Error";
import Dashboard from "./Page/Dashboard";
import Register from "./Page/Register";
import Login from "./Page/Login";
import CreateApp from "./Page/CreateApp";

const router = createBrowserRouter([
  {
    element: <Layout />,
    errorElement: <Error />,

    children: [
      {
        path: "/",
        element: <Dashboard />,
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
        element: <CreateApp />,
      },
    ],
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
