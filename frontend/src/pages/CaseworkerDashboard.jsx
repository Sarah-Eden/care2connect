import React, { useState } from "react";
import DashboardLayout from "../components/DashboardLayout";
import CaseList from "../components/CaseList";
import DetailView from "../components/DetailView";
import Navigation from "../components/Navigation";

export default function CaseworkerDashboard() {
  const [activeForm, setActiveForm] = useState(null);
  const [selectedCase, setSelectedCase] = useState(null);

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
      role="Caseworker"
      navigation={
        <Navigation role="Caseworker" onFormSelect={handleFormSelect} />
      }
      caseList={<CaseList onSelect={handleCaseSelect} />}
      detailView={
        <DetailView
          selectedCase={selectedCase}
          activeForm={activeForm}
          onCloseForm={() => setActiveForm(null)}
        />
      }
    />
  );
}
