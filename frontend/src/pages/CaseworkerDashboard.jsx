import React, { useState } from "react";
import DashboardLayout from "../components/DashboardLayout";
import CaseList from "../components/CaseList";
import DetailView from "../components/DetailView";
import NewCaseForm from "../components/NewCaseForm";
import Notifications from "../components/Notifications";
import logo from "../assets/C2C_Logo_no_bg.png";
import api from "../api";

export default function CaseworkerDashboard() {
  const [activeView, setActiveView] = useState({ type: "detail", data: null });
  const [selectedCase, setSelectedCase] = useState(null);

  return (
    <DashboardLayout
      role="Caseworker"
      caseList={<CaseList onSelect={setSelectedCase} />}
      detailView={<DetailView selectedCase={selectedCase} />}
      notifications={<Notifications />}
    />
  );
}
