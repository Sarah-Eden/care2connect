import React from "react";
import { Box, Typography, Grid, Divider } from "@mui/material";
import NewCaseForm from "./NewCaseForm";

export default function DetailView({ selectedCase }) {
  if (!selectedCase) {
    return <Typography>Select a case from the list.</Typography>; // Fallback if no selected
  }

  return (
    <Box sx={{ p: 2, backgroundColor: "#f7f7f7" }}>
      <Typography variant="h6" color="primary">
        Case Details
      </Typography>
      <Grid container spacing={2}>
        <Grid item xs={12} sm={6}>
          <Typography>
            Child: {selectedCase.child.first_name}{" "}
            {selectedCase.child.last_name}
          </Typography>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Typography>Status: {selectedCase.status}</Typography>
        </Grid>
      </Grid>
      <Box sx={{ p: 2, backgroundColor: "primary" }}>
        <NewCaseForm />
      </Box>
    </Box>
  );
}
