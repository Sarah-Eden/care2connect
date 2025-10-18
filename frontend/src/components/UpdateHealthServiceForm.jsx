import { useState } from "react";
import { useForm, Controller } from "react-hook-form";
import {
  Box,
  TextField,
  Button,
  Alert,
  Grid,
  InputLabel,
  MenuItem,
  Typography,
  FormControl,
  Select,
  FormHelperText,
} from "@mui/material";
import { updateHealthServiceRecord } from "../api";

export default function UpdateHealthServiceForm({
  healthService,
  onClose,
  onSuccess,
}) {
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const scheduledImmunizations = healthService.immunizations || [];
  const hasImmunizations = healthService.immunizations.length > 0;

  const {
    control,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm({
    defaultValues: {
      dateComplete: "",
      immunizations: scheduledImmunizations,
    },
  });

  const onSubmit = async (data) => {
    setError(null);
    console.log("Form data:", data);

    try {
      const updateData = {
        child: healthService.child.id,
        service: healthService.service,
        immunizations: data.immunizations || [],
        due_date: healthService.due_date,
        completed_date: data.dateComplete,
        status: data.status,
        created_date: healthService.created_date,
        updated_date: new Date().toISOString().split("T")[0],
      };

      console.log("Update data being sent:", updateData);

      await updateHealthServiceRecord(healthService.id, updateData);
      setSuccess(true);
      if (onSuccess) {
        onSuccess();
      }
      setTimeout(() => onClose(), 1500);
    } catch (error) {
      console.error("Full error response:", error.response);
      console.error("Error data", error.response?.data);
      console.error("Error status", error.response?.status);
      console.error("Error updating health service record.", error);
      setError("Failed to update health service record.");
    }
  };

  return (
    <Box>
      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          Health service record update success.
        </Alert>
      )}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <form onSubmit={handleSubmit(onSubmit)}>
        <Grid container spacing={2}>
          <Grid item size={{ xs: 12 }}>
            <Controller
              name="dateComplete"
              control={control}
              rules={{ required: "Completed date is required." }}
              render={({ field }) => (
                <TextField
                  {...field}
                  label="Completed Date"
                  type="date"
                  fullWidth
                  slotProps={{ inputLabel: { shrink: true } }}
                  error={!!errors.completed_date}
                  helperText={errors.completed_date?.message}
                />
              )}
            />
          </Grid>
          {hasImmunizations ? (
            <Grid item size={{ xs: 12 }}>
              <FormControl fullWidth error={!!errors.immunizations}>
                <InputLabel>Immunizations Given</InputLabel>
                <Controller
                  name="immunizations"
                  control={control}
                  defaultValue={[]}
                  render={({ field }) => (
                    <Select
                      {...field}
                      multiple
                      label="Immunizations Given"
                      value={field.value || []}
                    >
                      {healthService.immunizations.map((value) => (
                        <MenuItem key={value} value={value}>
                          {value}
                        </MenuItem>
                      ))}
                    </Select>
                  )}
                />
                {errors.immunizations && (
                  <Typography color="error">
                    {errors.immunizations.message}
                  </Typography>
                )}
              </FormControl>
            </Grid>
          ) : (
            <Grid item size={{ xs: 12 }}>
              <Typography variant="body2" color="text.secondary">
                No immunizations scheduled for this visit.
              </Typography>
            </Grid>
          )}

          <Grid item size={{ xs: 12 }}>
            <Controller
              name="status"
              control={control}
              defaultValue="complete"
              render={({ field }) => (
                <FormControl fullWidth error={!!errors.status}>
                  <InputLabel>Status</InputLabel>
                  <Select {...field} label="Status">
                    <MenuItem value="pending">Pending</MenuItem>
                    <MenuItem value="complete">Complete</MenuItem>
                  </Select>
                  {errors.status && (
                    <FormHelperText>{errors.status.message}</FormHelperText>
                  )}
                </FormControl>
              )}
            />
          </Grid>
        </Grid>

        {/* Form buttons */}
        <Box sx={{ display: "flex", gap: 2, justifyContent: "flex-end" }}>
          <Button
            variant="outlined"
            color="secondary"
            onClick={() => {
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
