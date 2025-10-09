import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import SupervisorDashboard from "./pages/SupervisorDashboard";
import CaseworkerDashboard from "./pages/CaseworkerDashboard";
import FosterParentDashboard from "./pages/FosterParentDashboard";
import ProtectedRoute from "./components/ProtectedRoute";
import Dashboard from "./pages/Dashboard";
import { GROUPS } from "./constants";

function Logout() {
  localStorage.clear();
  return <Navigate to="/login" />;
}

function RoleDashboard() {
  const groups = JSON.parse(localStorage.getItem(GROUPS) || "[]");
  const role = groups[0];

  if (!role) {
    return <Navigate to="/login" />;
  }

  return <Dashboard role={role} />;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
export default App;
