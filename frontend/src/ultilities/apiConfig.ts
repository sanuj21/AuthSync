import axios from "axios";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_URL,
});

// Request interceptor to attach the access token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor to handle token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem("refresh");
        console.log("Refreshing token...", refreshToken);
        const { data } = await axios.post(
          `${import.meta.env.VITE_BACKEND_URL}/api/token/refresh/`,
          { refresh: refreshToken }
        );

        localStorage.setItem("access", data.access);
        originalRequest.headers.Authorization = `Bearer ${data.access}`;

        return apiClient(originalRequest);
      } catch (err) {
        console.error("Token refresh failed:", err);
        // Handle logout or redirect to login
        localStorage.clear();
        window.location.href = "/login";
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
