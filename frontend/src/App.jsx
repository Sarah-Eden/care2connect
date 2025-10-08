import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import SupervisorDashboard from "./pages/SupervisorDashboard";
import CaseworkerDashboard from "./pages/CaseworkerDashboard";
import FosterParentDashboard from "./pages/FosterParentDashboard";
import ProtectedRoute from "./components/ProtectedRoute";

function Logout() {
  localStorage.clear();
  return <Navigate to="/login" />;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />
        <Route
          path="/sup-dashboard"
          element={
            <ProtectedRoute>
              <SupervisorDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/cw-dashboard"
          element={
            <ProtectedRoute>
              <CaseworkerDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/fp-dashboard"
          element={
            <ProtectedRoute>
              <FosterParentDashboard />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
export default App;
