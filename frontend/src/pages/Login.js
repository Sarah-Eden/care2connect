import React, { useState } from "react";
import api from "../api";
import { ACCESS_TOKEN, REFRESH_TOKEN, GROUPS } from "../constants";
import { useNavigate } from "react-router-dom";
import {
  Box,
  Button,
  TextField,
  Typography,
  Card,
  CardContent,
  Alert,
} from "@mui/material";
import logo from "../assets/C2C_Logo_no_bg.png";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await api.post("/api/token/", { username, password });
      console.log("Login response", res.data);

      const userGroups = res.data.groups || [];
      localStorage.setItem(ACCESS_TOKEN, res.data.access);
      localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
      localStorage.setItem(GROUPS, JSON.stringify(res.data.groups));

      // Will redirect to appropriate dashboard
      if (userGroups.includes("Supervisor")) {
        navigate("/SupervisorDashboard");
      } else if (userGroups.includes("Caseworker")) {
        navigate("/CaseworkerDashboard");
      } else if (userGroups.incluudes("FosterParent")) {
        navigate("/FosterParentDashboard");
      } else {
        alert("No recognized role for account - redirecting to login.");
        navigate("/");
      }
    } catch (error) {
      alert(error);
    }
  };

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        backgroundColor: "background.default",
        padding: { xs: 2, sm: 4 },
      }}
    >
      <Card
        sx={{
          width: { xs: "100%", sm: "400px" },
          maxWidth: "400px",
          padding: 2,
          boxShadow: 3,
        }}
      >
        <CardContent>
          <Box sx={{ textAlign: "center", mb: 1 }}>
            <img
              src={logo}
              alt="Care2Connect Logo"
              style={{ maxWidth: "200px" }}
            />
          </Box>
          <Typography
            variant="h5"
            align="center"
            gutterBottom
            color="text.primary"
          >
            Login
          </Typography>
          <form onSubmit={handleSubmit}>
            <TextField
              label="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              fullWidth
              margin="normal"
              color="secondary"
              required
            />
            <TextField
              label="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              fullWidth
              margin="normal"
              color="secondary"
              required
            />
            <Button
              type="submit"
              variant="contained"
              size="large"
              color="primary"
              fullWidth
              sx={{ mt: 2 }}
            >
              Login
            </Button>
          </form>
        </CardContent>
      </Card>
    </Box>
  );
}

export default Login;
