import axios from "axios";
import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import apiClient from "../ultilities/apiConfig";

const formatDate = (date: string) => {
  const d = new Date(date);
  return `Subscription Ends on : ${d.getDate()}/${
    d.getMonth() + 1
  }/${d.getFullYear()}`;
};

function Dashboard() {
  const [myAppData, setMyAppData] = useState([]);

  useEffect(() => {
    const getMyAppData = async () => {
      try {
        const res = await apiClient({
          method: "get",
          url: "/api/client-app/",
        });

        setMyAppData(res.data);

        console.log(res);
      } catch (error) {
        console.log(console.error());
      }
    };

    getMyAppData();
  }, []);

  return (
    <div className="h-screen m-10">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {myAppData.map((app: any) => (
          <div
            key={app.id}
            className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6"
          >
            <h2 className="text-lg font-semibold text-gray-800 dark:text-white">
              {app.name}
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mt-2">
              {app.description}
            </p>

            <p className="text-gray-600 dark:text-gray-400 mt-2">
              {app.no_of_users} users
            </p>

            <p className="text-gray-600 dark:text-gray-400 mt-2">
              {app.subscriptions?.some((sub) => sub.is_active)
                ? app.subscriptions.find((sub) => sub.is_active)?.plan.name
                : "No active subscription"}
            </p>

            {/* display ending date */}
            <p className="text-gray-600 dark:text-gray-400 mt-2">
              {app.subscriptions?.some((sub) => sub.is_active)
                ? formatDate(
                    app.subscriptions.find((sub) => sub.is_active)?.end_date
                  )
                : ""}
            </p>

            <div className="mt-4">
              <Link
                to={`/editConfig/${app.id}`}
                className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
              >
                Edit Configurations
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Dashboard;
