import axios from "axios";
import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import apiClient from "../ultilities/apiConfig";

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
    <div>
      <div>
        <Link to="/createApp">Create a New App</Link>
      </div>
    </div>
  );
}

export default Dashboard;
