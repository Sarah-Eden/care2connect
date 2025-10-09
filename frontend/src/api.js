import axios from "axios";
import { ACCESS_TOKEN } from "./constants";

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

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error: ", error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Children
export const getChildren = async () => {
  try {
    const res = await api.get("/api/children/");
    return res.data;
  } catch (error) {
    console.error("Error fetching children: ", error);
    throw error;
  }
};

export const getChild = async (id) => {
  if (!id) throw new Error("Child ID is required");
  try {
    const res = await api.get(`/api/children/${id}/`);
    return res.data;
  } catch (error) {
    console.error(`Error fetching child ${id}: `, error);
    throw error;
  }
};

export const createChild = async (childData) => {
  try {
    const res = await api.post("/api/children/", childData);
    return res.data;
  } catch (error) {
    console.error("Error creating child: ", error);
    throw error;
  }
};

export const updateChild = async (id, childData) => {
  try {
    const res = await api.patch(`/api/children/${id}/`, childData);
    return res.data;
  } catch (error) {
    console.error("Error updating child: ", error);
    throw error;
  }
};

// CASES
export const getCases = async () => {
  try {
    const res = await api.get("/api/cases/");
    return res.data;
  } catch (error) {
    console.error("Error fetching cases: ", error);
    throw error;
  }
};

export const getCase = async (id) => {
  if (!id) throw new Error("Case ID is required");
  try {
    const res = await api.get(`/api/cases/${id}/`);
    return res.data;
  } catch (error) {
    console.error(`Error fetching case ${id}: `, error);
    throw error;
  }
};

export const createCase = async (caseData) => {
  try {
    const res = await api.post("/api/cases/", caseData);
    return res.data;
  } catch (error) {
    console.error("Error creating case: ", error);
    throw error;
  }
};

export const updateCase = async (id, caseData) => {
  try {
    const res = await api.patch(`/api/cases/${id}/`, caseData);
    return res.data;
  } catch (error) {
    console.error("Error updating child: ", error);
    throw error;
  }
};

// Foster Families
export const getFosterFamilies = async () => {
  try {
    const res = await api.get("/api/foster-families/");
    return res.data;
  } catch (error) {
    console.error("Error fetching foster families: ", error);
    throw error;
  }
};

export const getFosterFamily = async (id) => {
  if (!id) throw new Error("Family ID is required");
  try {
    const res = await api.get(`/api/foster-families/${id}/`);
    return res.data;
  } catch (error) {
    console.error(`Error fetching foster families ${id}: `, error);
    throw error;
  }
};

export const createFosterFamily = async (familyData) => {
  try {
    const res = await api.post("/api/foster-families/", familyData);
    return res.data;
  } catch (error) {
    console.error("Error creating foster familiy: ", error);
    throw error;
  }
};

// Foster Placements
export const getFosterPlacements = async () => {
  try {
    const res = await api.get("/api/foster-placements/");
    return res.data;
  } catch (error) {
    console.error("Error fetching foster placements: ", error);
    throw error;
  }
};

export const getFosterPlacement = async (id) => {
  if (!id) throw new Error("Placement ID is required");
  try {
    const res = await api.get(`/api/foster-placements/${id}/`);
    return res.data;
  } catch (error) {
    console.error(`Error fetching foster placement ${id}: `, error);
    throw error;
  }
};

export const createFosterPlacement = async (placementData) => {
  try {
    const res = await api.post("/api/foster-placements/", placementData);
    return res.data;
  } catch (error) {
    console.error("Error creating foster placement: ", error);
    throw error;
  }
};

export const updateFosterPlacement = async (id, placementData) => {
  try {
    const res = await api.patch(`/api/foster-placements/${id}/`, placementData);
    return res.data;
  } catch (error) {
    console.error("Error updating child: ", error);
    throw error;
  }
};

// Health Service Records
export const getHealthServiceRecords = async () => {
  try {
    const res = await api.get("/api/health-services/");
    return res.data;
  } catch (error) {
    console.error("Error fetching health service records: ", error);
    throw error;
  }
};

export const getHealthServiceRecord = async (id) => {
  if (!id) throw new Error("Case ID is required");
  try {
    const res = await api.get(`/api/health-services/${id}/`);
    return res.data;
  } catch (error) {
    console.error(`Error fetching health service record ${id}: `, error);
    throw error;
  }
};

export const createHealthServiceRecord = async (healthServiceData) => {
  try {
    const res = await api.post("/api/health-services/", healthServiceData);
    return res.data;
  } catch (error) {
    console.error("Error creating health service record: ", error);
    throw error;
  }
};

export const updateHealthServiceRecord = async (id, healthServiceData) => {
  try {
    const res = await api.patch(
      `/api/health-services/${id}/`,
      healthServiceData
    );
    return res.data;
  } catch (error) {
    console.error("Error updating health service record: ", error);
    throw error;
  }
};

// Immunization Records
export const getImmunizationRecords = async () => {
  try {
    const res = await api.get("/api/immunization-records/");
    return res.data;
  } catch (error) {
    console.error("Error fetching immunization records: ", error);
    throw error;
  }
};

export const getImmunizationRecord = async (id) => {
  if (!id) throw new Error("Immunization Record ID is required");
  try {
    const res = await api.get(`/api/immunization-records/${id}/`);
    return res.data;
  } catch (error) {
    console.error(`Error fetching immunization record ${id}: `, error);
    throw error;
  }
};

export const createImmunizationRecord = async (immunizationData) => {
  try {
    const res = await api.post("/api/immunization-records/", immunizationData);
    return res.data;
  } catch (error) {
    console.error("Error creating immunization record: ", error);
    throw error;
  }
};

export const updateImmunizationRecord = async (id, immunizationData) => {
  try {
    const res = await api.patch(
      `/api/immunization-records/${id}/`,
      immunizationData
    );
    return res.data;
  } catch (error) {
    console.error("Error updating immunization record: ", error);
    throw error;
  }
};

// Reminder Logs
export const getReminderLogs = async () => {
  try {
    const res = await api.get("/api/reminders");
    return res.data;
  } catch (error) {
    console.error("Error fetching reminder logs: ", error);
    throw error;
  }
};

// Helper functions
// Get all health service records due in the next 30 days
export const getUpcomingHealthServiceRecords = async () => {
  try {
    const allServices = await getHealthServiceRecords();
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const thirtyDaysFromToday = new Date(
      today.getTime() + 30 * 24 * 60 * 60 * 1000
    );

    // Debug
    console.log("=== getUpcomingHealthServiceRecords Debug ===");
    console.log("All services:", allServices);
    console.log("Today:", today);
    console.log("30 days from now", thirtyDaysFromToday);

    const filtered = allServices.filter((service) => {
      const dueDate = new Date(service.due_date);
      const isPending = service.status === "pending";
      const isWithin30Days = dueDate >= today && dueDate <= thirtyDaysFromToday;

      console.log(`Service ${service.id}:`, {
        due_date: service.due_date,
        dueDate,
        status: service.status,
        isPending,
        isWithin30Days,
        willInclude: isPending && isWithin30Days,
      });
      return isPending && isWithin30Days;
    });

    console.log("Filtered upcoming services", filtered);
    return filtered;
  } catch (error) {
    console.error("Error fetching upcoming health services:", error);
    throw error;
  }
};

// Get overdue health services
export const getOverdueHealthServiceRecords = async () => {
  try {
    const allServices = await getHealthServiceRecords();
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    return allServices.filter((service) => {
      const dueDate = new Date(service.due_date);
      return service.status === "pending" && dueDate < today;
    });
  } catch (error) {
    console.error("Error fetching overdue health service records: ", error);
    throw error;
  }
};

export default api;
