import { useState, useEffect } from "react";
import DashboardLayout from "../components/DashboardLayout";
import CaseList from "../components/CaseList";
import DetailView from "../components/DetailView";
import Navigation from "../components/Navigation";
import { GROUPS } from "../constants";

export default function Dashboard() {
  const [activeForm, setActiveForm] = useState(null);
  const [selectedCase, setSelectedCase] = useState(null);
  const [caseRefresh, setCaseRefresh] = useState(0);
  const [userRole, setUserRole] = useState(null);

  // Get user role on page load
  useEffect(() => {
    const groups = JSON.parse(localStorage.getItem(GROUPS) || "[]");
    setUserRole(groups[0] || "Unknown");
  }, []);

  const handleFormSelect = (formType) => {
    setActiveForm(formType);
    setSelectedCase(null);
  };

  const handleCaseSelect = (caseData) => {
    setSelectedCase(caseData);
    setActiveForm(null);
  };

  return (
    <DashboardLayout
      role={userRole}
      navigation={
        <Navigation role={userRole} onFormSelect={handleFormSelect} />
      }
      caseList={<CaseList onSelect={handleCaseSelect} refresh={caseRefresh} />}
      detailView={
        <DetailView
          selectedCase={selectedCase}
          activeForm={activeForm}
          onCloseForm={() => setActiveForm(null)}
          onCaseCreated={() => setCaseRefresh((prev) => prev + 1)}
        />
      }
    />
  );
}
