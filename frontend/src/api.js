import axios from "axios";
import { ACCESS_TOKEN } from "./constants";

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(ACCESS_TOKEN);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const getChildren = async () => {
  const res = await api.get("/api/children/");
  return res.data;
};

export const getChild = async (id) => {
  if (!id) throw new Error("Child ID is required");
  const res = await api.get(`/api/children/${id}/`);
  return res.data;
};

export const createChild = async (childData) => {
  const res = await api.post("/api/children/", childData);
  return res.data;
};

export const updateChild = async (id, childData) => {
  const res = await api.patch(`/api/children/${id}/`, childData);
  return res.data;
};

export const getCases = async () => {
  const res = await api.get("/api/cases/");
  return res.data;
};

export const getCase = async (id) => {
  if (!id) throw new Error("Case ID is required");
  const res = await api.get(`/api/cases/${id}/`);
  return res.data;
};

export const createCase = async (caseData) => {
  const res = await api.post("/api/cases/", caseData);
  return res.data;
};

export const updateCase = async (id, caseData) => {
  const res = await api.patch(`/api/cases/${id}/`, caseData);
  return res.data;
};

export const getFosterFamilies = async () => {
  const res = await api.get("/api/foster-families/");
  return res.data;
};

export const getFosterFamily = async (id) => {
  if (!id) throw new Error("Family ID is required");
  const res = await api.get(`/api/foster-families/${id}/`);
  return res.data;
};

export const createFosterFamily = async (familyData) => {
  const res = await api.post("/api/foster-families/", familyData);
  return res.data;
};

export const getFosterPlacements = async () => {
  const res = await api.get("/api/foster-placements/");
  return res.data;
};

export const getFosterPlacement = async (id) => {
  if (!id) throw new Error("Placement ID is required");
  const res = await api.get(`/api/foster-placements/${id}/`);
  return res.data;
};

export const createFosterPlacement = async (placementData) => {
  const res = await api.post("/api/foster-placements/", placementData);
  return res.data;
};

export const updateFosterPlacement = async (id, placementData) => {
  const res = await api.patch(`/api/foster-placements/${id}/`, placementData);
  return res.data;
};

export const getHealthServiceRecords = async () => {
  const res = await api.get("/api/health-services/");
  return res.data;
};

export const getHealthServiceRecord = async (id) => {
  if (!id) throw new Error("ID is required");
  const res = await api.get(`/api/health-services/${id}/`);
  return res.data;
};

export const createHealthServiceRecord = async (healthServiceData) => {
  const res = await api.post("/api/health-services/", healthServiceData);
  return res.data;
};

export const updateHealthServiceRecord = async (id, healthServiceData) => {
  const res = await api.patch(`/api/health-services/${id}/`, healthServiceData);
  return res.data;
};

export const getUsers = async () => {
  const res = await api.get("/api/users/");
  return res.data;
};

export const getUser = async (id) => {
  if (!id) throw new Error("User ID is required.");
  const res = await api.get(`/api/users/${id}/`);
  return res.data;
};

export const getUsersByGroup = async (groupName) => {
  const res = await api.get(`/api/users/?group=${groupName}`);
  return res.data;
};

export const createUser = async (userData) => {
  const res = await api.post("/api/users/", userData);
  return res.data;
};

export const getUpcomingHealthServiceRecords = async () => {
  const allServices = await getHealthServiceRecords();
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const thirtyDaysFromToday = new Date(
    today.getTime() + 30 * 24 * 60 * 60 * 1000,
  );

  return allServices.filter((service) => {
    const dueDate = new Date(service.due_date);
    return (
      service.status === "pending" &&
      dueDate >= today &&
      dueDate <= thirtyDaysFromToday
    );
  });
};

export const getOverdueHealthServiceRecords = async () => {
  const allServices = await getHealthServiceRecords();
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  return allServices.filter((service) => {
    const dueDate = new Date(service.due_date);
    return service.status === "pending" && dueDate < today;
  });
};

export default api;
