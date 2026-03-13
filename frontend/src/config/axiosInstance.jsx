import axios from "axios";
export const API_BASE = import.meta.env.VITE_REACT_APP_BACKEND_BASEURL;
const axiosInstance = axios.create({
  baseURL: API_BASE,
});

axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  const lang = localStorage.getItem("lang") || "en";
  config.headers["Accept-Language"] = lang;
  
  return config;
});

export default axiosInstance;
