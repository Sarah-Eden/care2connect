import axios from "axios";
import { ACCESS_TOKEN } from "./constants";
import jwtDecode from "jwt-decode";

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
});

// Interceptor to add token to every request if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log("Added token to request:", config.url);
    } else {
      console.warn("No token found for request:", config.url);
    }
    return config;
  },
  (error) => {
    console.error("Interceptor error:", error);
    return Promise.reject(error);
  }
);

// Fetch all children
export const getChildren = async () => {
  try {
    const res = await api.get("/api/children");
    if (!Array.isArray(res.data)) {
      throw new Error("Invalid data format: expected array");
    }
    return res.data;
  } catch (error) {
    console.error("Error fetching children", error);
  }
};

// Get one child's information
export const getChild = async (id) => {
  if (!id) throw new Error("Child ID is required");
  try {
    const res = await api.get("/api/children");
    if (!Array.isArray(res.data)) {
      throw new Error("Invalid data format: expected array");
    }
    return res.data;
  } catch (error) {
    console.error("Error fetching children", error);
  }
};

// Fetch all

export default api;
