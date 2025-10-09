import React from "react";
import { Box, Typography, Grid, Divider, IconButton } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import NewCaseForm from "./NewCaseForm";
import NewPlacementForm from "./NewPlacementForm";

export default function DetailView({ selectedCase, activeForm, onCloseForm }) {
  if (activeForm) {
    return (
      <Box sx={{ p: 2 }}>
        {/*Form header with close button */}
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            mb: 2,
          }}
        >
          <Typography variant="h6" color="primary">
            {activeForm === "add_case" && "Add New Case"}
            {activeForm === "add_placement" && "Add New Placement"}
            {activeForm === "add_child" && "Add New Child"}
            {activeForm === "add_foster_family" && "Add New Foster Family"}
            {activeForm === "enter_health_visit" && "Enter Health Visit"}
          </Typography>
          <IconButton onClick={onCloseForm} size="small">
            <CloseIcon />
          </IconButton>
        </Box>

        {/*Render appropriate form */}
        {activeForm === "add_case" && <NewCaseForm onClose={onCloseForm} />}
        {activeForm === "add_placement" && (
          <NewPlacementForm onClose={onCloseForm} />
        )}
      </Box>
    );
  }

  if (selectedCase) {
    const child = selectedCase.child;

    return (
      <Box sx={{ p: 2 }}>
        <Typography variant="h5" color="primary" gutterBottom>
          {child.first_name} {child.last_name}
        </Typography>

        <Divider sx={{ my: 2 }} />

        <Grid container spacing={2}>
          <Grid item size={{ xs: 12, sm: 6 }}>
            <Typography variant="subtitle2" color="text.secondary">
              Date of Birth
            </Typography>
            <Typography variant="body1">
              {new Date(child.dob).toLocaleDateString()}
            </Typography>
          </Grid>

          <Grid item size={{ xs: 12, sm: 6 }}>
            <Typography variant="subtitle2" color="text.secondary">
              Case Status
            </Typography>
            <Typography variant="body1" sx={{ textTansform: "capitalize" }}>
              {selectedCase.status}
            </Typography>
          </Grid>

          <Grid item size={{ xs: 12 }}>
            <Typography variant="subtitle2" color="text.secondary" gutterBottom>
              Allergies
            </Typography>
            <Typography variant="body1">
              {child.allergies || "None Listed"}
            </Typography>
          </Grid>

          <Grid item size={{ xs: 12 }}>
            <Typography variant="subtitle2" color="text.secondary" gutterBottom>
              Medications
            </Typography>
            <Typography variant="body1">
              {child.medications || "None Listed"}
            </Typography>
          </Grid>

          <Grid item size={{ xs: 12 }}>
            <Typography variant="subtitle2" color="text.secondary">
              Case Start Date
            </Typography>
            {new Date(selectedCase.start_date).toLocaleDateString()}
          </Grid>
        </Grid>
      </Box>
    );
  }

  {
    /* Nothing selected (Default) */
  }
  return (
    <Box
      sx={{
        p: 4,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        height: "100%",
      }}
    >
      <Typography variant="h6" color="text.secondary" textAlign={"center"}>
        Select a case from the list or choose an action from the menu.
      </Typography>
    </Box>
  );
}
