import { useState, useEffect } from "react";
import { useForm, Controller } from "react-hook-form";
import {
  Box,
  Typography,
  TextField,
  Button,
  Alert,
  Grid,
  Card,
  CardContent,
  MenuItem,
} from "@mui/material";
import { createUser } from "../api";

export default function NewUserForm({ onClose, onSuccess }) {
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [tempPassword, setTempPassword] = useState(null);

  const {
    control,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm({
    defaultValues: {
      username: "",
      email: "",
      firstName: "",
      lastName: "",
      role: "",
    },
  });

  const onSubmit = async (data) => {
    setError(null);

    try {
      const tempPass = `C@C-${Math.random().toString(36).slice(2, 10)}`;

      const userData = {
        username: data.username,
        password: tempPass,
        email: data.email,
        first_name: data.firstName,
        last_name: data.lastName,
        groups: [parseInt(data.role)],
        is_active: true,
      };

      await createUser(userData);
      setSuccess(true);
      setTempPassword(tempPass);

      if (onSuccess) onSuccess();
    } catch (error) {
      if (error.response?.data) {
        const message = Object.values(error.response.data).flat().join(" ");
        setError(message);
      } else {
        setError("Failed to create user account.");
      }
    }
  };

  return (
    <Box sx={{ p: 2 }}>
      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          Account createrd. Temporary password: <strong>{tempPassword}</strong>
          <br />
          Please provide this to the user.
        </Alert>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {!success && (
        <form onSubmit={handleSubmit(onSubmit)}>
          <Card elevation={2} sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" color="primary" gutterBottom>
                New User Account
              </Typography>

              <Grid container spacing={2}>
                <Grid item size={{ xs: 12, sm: 6 }}>
                  <Controller
                    name="firstName"
                    control={control}
                    rules={{ required: "First name is required." }}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        label="First Name"
                        fullWidth
                        required
                        error={!!errors.firstName}
                        helperText={errors.firstName?.message}
                      />
                    )}
                  />
                </Grid>

                <Grid item size={{ xs: 12, sm: 6 }}>
                  <Controller
                    name="lastName"
                    control={control}
                    rules={{ required: "Last name is required." }}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        label="Last Name"
                        fullWidth
                        required
                        error={!!errors.lastName}
                        helperText={errors.lastName?.message}
                      />
                    )}
                  />
                </Grid>

                <Grid item size={{ xs: 12 }}>
                  <Controller
                    name="email"
                    control={control}
                    rules={{
                      required: "Email is required.",
                      pattern: {
                        value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                        message: "Enter a valid email address.",
                      },
                    }}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        label="Email"
                        type="email"
                        fullWidth
                        required
                        error={!!errors.email}
                        helperText={errors.email?.message}
                      />
                    )}
                  />
                </Grid>

                <Grid item size={{ xs: 12 }}>
                  <Controller
                    name="username"
                    control={control}
                    rules={{
                      required: "Username is required.",
                      minLength: {
                        value: 6,
                        message: "Username must be at least 6 characters.",
                      },
                    }}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        label="Username"
                        fullWidth
                        required
                        errors={!!errors.username}
                        helperText={errors.username?.message}
                      />
                    )}
                  />
                </Grid>

                <Grid item size={{ xs: 12 }}>
                  <Controller
                    name="role"
                    control={control}
                    rules={{ required: "Role is required." }}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        select
                        label="Role"
                        fullWidth
                        required
                        error={!!errors.role}
                        helperText={errors.role?.message}
                      >
                        <MenuItem value="" disabled>
                          Select a role
                        </MenuItem>
                        <MenuItem value="1">Supervisor</MenuItem>
                        <MenuItem value="2">Caseworker</MenuItem>
                        <MenuItem value="3">Foster Parent</MenuItem>
                      </TextField>
                    )}
                  />
                </Grid>
              </Grid>
            </CardContent>
          </Card>

          <Box sx={{ display: "flex", gap: 2, justifyContent: "flex-end" }}>
            <Button
              variant="outlined"
              color="secondary"
              onClick={() => {
                reset();
                onClose();
              }}
              disabled={isSubmitting}
            >
              Cancel
            </Button>

            <Button
              type="submit"
              variant="contained"
              color="primary"
              disabled={isSubmitting}
            >
              Create Account
            </Button>
          </Box>
        </form>
      )}
    </Box>
  );
}
