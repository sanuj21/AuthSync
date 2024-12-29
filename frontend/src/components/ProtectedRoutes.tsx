import axios from "axios";
import { ReactNode, useEffect, useState } from "react";
import { refreshTokenIfAccessExpired } from "../ultilities/tokenRefresh";
import { useNavigate } from "react-router-dom";

export const ProtectedRoute: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuth = async () => {
      const refreshToken = localStorage.getItem("refresh");
      if (!refreshToken) {
        navigate("/login");
        return;
      }

      try {
        const { data } = await axios.post(
          `${import.meta.env.VITE_BACKEND_URL}/api/token/refresh/`,
          { refresh: refreshToken }
        );
        localStorage.setItem("access", data.access);
      } catch (err) {
        console.error("Proactive token refresh failed:", err);
        localStorage.clear();
        navigate("/login");
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  if (isLoading) return null;

  return children;
};
