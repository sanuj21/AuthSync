import axios from "axios";
import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function Dashboard() {
  const [myAppData, setMyAppData] = useState([]);

  useEffect(() => {
    const getMyAppData = async () => {
      try {
        const res = await axios({
          method: "get",
          url: import.meta.env.VITE_BACKEND_URL + "/api/client-app/",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
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
