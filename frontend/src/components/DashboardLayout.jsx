import React from "react";
import {
  Box,
  AppBar,
  Toolbar,
  Typography,
  Button,
  Grid,
  Paper,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import CaseList from "./CaseList";
import Notifications from "./Notifications";
import Navigation from "./Navigation";

export default function DashboardLayout({ role, caseList, detailView }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        height: "100vh",
      }}
    >
      <AppBar position="static" color="primary">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            {role} Dashboard
          </Typography>
          <Button color="inherit" onClick={handleLogout}>
            Logout
          </Button>
        </Toolbar>
      </AppBar>
      <Box sx={{ flexGrow: 1 }}>
        <Grid container spacing={0.5} sx={{ height: "100%", p: 2 }}>
          <Grid item size={{ xs: 12, md: 2 }}>
            <Paper
              elevation={5}
              sx={{
                width: "100%",
                height: "100%",
                backgroundColor: "#f7f7f7",
              }}
            >
              <Navigation role={role} />
            </Paper>
          </Grid>
          <Grid item size={{ xs: 12, md: 3 }}>
            <Paper elevation={3} sx={{ width: "100%", height: "100%" }}>
              {caseList}
            </Paper>
          </Grid>
          <Grid item size={{ xs: 12, md: 5 }}>
            <Paper
              elevation={3}
              sx={{
                width: "100%",
                height: "100%",
                backgroundColor: "#f7f7f7",
              }}
            >
              {detailView}
            </Paper>
          </Grid>
          <Grid item size={{ xs: 12, md: 2 }}>
            <Paper elevation={3} sx={{ width: "100%", height: "100%" }}>
              <Notifications />
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Box>
  );
}
