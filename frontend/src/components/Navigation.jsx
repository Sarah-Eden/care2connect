import { useState } from "react";
import { Box, Button, List, ListItem } from "@mui/material";
import logo from "../assets/C2C_Logo_no_bg.png";

export default function Navigation({ role, onFormSelect }) {
  const buttons =
    {
      Supervisors: [
        { label: "Add Child", formType: "add_child" },
        { Label: "Add Foster Family", formType: "add_foster_family" },
        { label: "Add Case", formType: "add_case" },
        { label: "Add Placement", formType: "add_placement" },
      ],
      Caseworker: [
        { label: "Add Case", formType: "add_case" },
        { label: "Add Placement", formType: "add_placement" },
      ],
      FosterParent: [
        { label: "Enter Health Visit", formType: "enter_health_visit" },
        { label: "Update Medications", formType: "update_medications" },
      ],
    }[role] || [];

  return (
    <Box sx={{ p: 2 }}>
      <Box sx={{ textAlign: "center", mb: 2 }}>
        <img
          src={logo}
          alt="Care2Connect Logo"
          style={{
            width: "100%",
            mb: 2,
          }}
        />
      </Box>

      {buttons.map((btn) => (
        <Button
          key={btn.formType}
          onClick={() => onFormSelect(btn.formType)}
          variant="contained"
          color="primary"
          fullWidth
          sx={{ mt: 2 }}
        >
          {btn.label}
        </Button>
      ))}
    </Box>
  );
}
