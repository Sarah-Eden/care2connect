import { useState } from "react";
import { useForm, Controller } from "react-hook-form";
import { Box, TextField, Button, Alert, Grid } from "@mui/material";
import { updateChild } from "../api";

export default function UpdateMedicalForm({ child, onClose, onSuccess }) {
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const {
    control,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm({
    defaultValues: {
      medications: child.medications,
      allergies: child.allergies,
    },
  });

  const onSubmit = async (data) => {
    setError(null);

    try {
      const updateData = {
        first_name: child.first_name,
        last_name: child.last_name,
        dob: child.dob,
        medications: data.medications?.trim() || null,
        allergies: data.allergies?.trim() || null,
      };

      await updateChild(child.id, updateData);
      setSuccess(true);

      if (onSuccess) {
        onSuccess();
      }

      setTimeout(() => {
        onClose();
      }, 1500);
    } catch (error) {
      console.error("Error updating child medical information:", error);
      setError("Failed to update medical information");
    }
  };

  return (
    <Box>
      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          Medical information updated successfully.
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
              name="allergies"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  label="Allergies"
                  multiline
                  rows={4}
                  fullWidth
                  placeholder="List food and environmental allergies."
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
                  label="Medications"
                  multiline
                  rows={4}
                  fullWidth
                  placeholder="List current medications..."
                />
              )}
            />
          </Grid>
        </Grid>

        <Box
          sx={{ display: "flex", gap: 2, mt: 3, justifyContent: "flex-end" }}
        >
          <Button
            variant="outlined"
            color="secondary"
            onClick={onClose}
            disabled={isSubmitting}
          >
            Cancel
          </Button>
          <Button
            variant="contained"
            type="submit"
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
