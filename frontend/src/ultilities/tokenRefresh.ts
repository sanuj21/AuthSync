import axios from "axios";

export const scheduleTokenRefresh = () => {
  const refreshToken = localStorage.getItem("refresh");
  if (!refreshToken) return;

  const refreshInterval = 5 * 60 * 1000; // 5 minutes before expiry

  setInterval(async () => {
    try {
      const { data } = await axios.post(
        `${import.meta.env.VITE_BACKEND_URL}/api/token/refresh/`,
        { refresh: refreshToken }
      );
      localStorage.setItem("access", data.access);
    } catch (err) {
      console.error("Proactive token refresh failed:", err);
      localStorage.clear();
      window.location.href = "/login";
    }
  }, refreshInterval);
};
