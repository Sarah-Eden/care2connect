import { useState } from "react";
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
} from "@mui/material";
import { createChild } from "../api";

export default function NewChildForm({ onClose, onSuccess }) {
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const {
    control,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
    watch,
  } = useForm({
    defaultValues: {
      firstName: "",
      lastName: "",
      dob: "",
      medications: "",
      allergies: "",
    },
  });

  const onSubmit = async (data) => {
    setError(null);

    try {
      const childData = {
        first_name: data.firstName,
        last_name: data.lastName,
        dob: data.dob,
      };

      if (data.medications?.trim()) {
        childData.medications = data.medications.trim();
      }

      if (data.allergies?.trim()) {
        childData.allergies = data.allergies.trim();
      }

      await createChild(childData);
      setSuccess(true);

      if (onSuccess) {
        onSuccess();
      }

      setTimeout(() => {
        onClose();
      }, 1500);
    } catch (error) {
      console.error("Error creating child:", error);
      setError("Failed to create child record.");
    }
  };

  return (
    <Box sx={{ p: 2 }}>
      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          Child record created successfully.
        </Alert>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <form onSubmit={handleSubmit(onSubmit)}>
        <Card elevation={2} sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" color="primary" gutterBottom>
              New Child Information
            </Typography>

            <Grid container spacing={2}>
              <Grid item size={{ xs: 12, sm: 6 }}>
                <Controller
                  name="firstName"
                  control={control}
                  rules={{
                    required: "First name is required.",
                    minLength: {
                      value: 2,
                      message: "First name must be at least 2 characters.",
                    },
                  }}
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
                  rules={{
                    required: "Last name is required.",
                    minLength: {
                      value: 2,
                      message: "Last name must be at least 2 characters.",
                    },
                  }}
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
                  name="dob"
                  control={control}
                  rules={{
                    required: "Date of birth is required",
                    validate: {
                      notFuture: (value) => {
                        const today = new Date().toISOString().split("T")[0];
                        if (value > today) {
                          return "Date of birth cannot be in the future.";
                        }
                        return true;
                      },
                      reasonable: (value) => {
                        const birthDate = new Date(value);
                        const today = new Date();
                        const age =
                          today.getFullYear() - birthDate.getFullYear();
                        if (age > 21) {
                          return "Child must be less than 21 years of age";
                        }
                        return true;
                      },
                    },
                  }}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Date of Birth"
                      type="date"
                      fullWidth
                      required
                      slotProps={{ inputLabel: { shrink: true } }}
                      error={!!errors.dob}
                      helperText={errors.dob?.message}
                    />
                  )}
                />
              </Grid>

              <Grid item size={{ xs: 12 }}>
                <Controller
                  name="medications"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Medications (Optional)"
                      multiline
                      rows={3}
                      fullWidth
                      placeholder="Enter current medications..."
                      helperText="Include medication name, dosage, and frequency."
                    />
                  )}
                />
              </Grid>

              <Grid item size={{ xs: 12 }}>
                <Controller
                  name="allergies"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Allergies (Optional)"
                      multiline
                      rows={3}
                      fullWidth
                      placeholder="Enter current allergies..."
                      helperText="Include both food and environmental allergies."
                    />
                  )}
                />
              </Grid>
            </Grid>
          </CardContent>
        </Card>

        {/* Form Buttons */}
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
            Submit
          </Button>
        </Box>
      </form>
    </Box>
  );
}
