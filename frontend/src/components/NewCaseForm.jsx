import { useState, useEffect } from "react";
import { Box, Typography, TextField, Button, Alert } from "@mui/material";
import api from "../api";

export default function NewCaseForm() {
  const [child, setChild] = useState(null);
  const [caseworker, setCaseworker] = useState(null);
  const [placement, setPlacement] = useState(null);
  const [startDate, setStartDate] = useState(null);
  const [status, setStatus] = useState("");
  const [childOptions, getChildOptions] = useState([]);
  const [caseworkerOptions, getCaseworkerOptions] = useState([]);
  const [placementOptions, getPlacementOptions] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await api.post("/api/cases/", {
        child,
        caseworker,
        placement,
        startDate,
        status,
      });
    } catch (error) {
      alert(error);
    }

    return (
      <Box sx={{ p: 2, backgroundColor: "background.paper" }}>
        <Typography variant="h6" color="primary">
          Add New Case
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            name="child"
            label="Child ID"
            onChange={(e) => setChild(e.target.value)}
          />
        </form>
      </Box>
    );
  };
}
