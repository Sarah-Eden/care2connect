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
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormHelperText,
  getFormLabelUtilityClasses,
} from "@mui/material";
import { getUsersByGroup, createFosterFamily } from "../api";

export default function NewFosterFamilyForm({ onClose, onSuccess }) {
  const [fosterParents, setFosterParents] = useState([]);
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
      familyName: "",
      parent1Id: "",
      parent2Id: "",
      maxOccupancy: 1,
    },
  });

  const parent1Id = watch("parent1Id");

  // Load Foster Parents
  useEffect(() => {
    const fetchFosterParents = async () => {
      try {
        const fosterParentUsers = await getUsersByGroup("FosterParent");
        setFosterParents(fosterParentUsers);
      } catch (error) {
        console.error("Error fetching Foster Parents:", error);
        setError("Failed to load Foster Parents.");
      }
    };
    fetchFosterParents();
  }, []);

  const onSubmit = async (data) => {
    setError(null);

    // Prevent same parent from being selected twice
    if (data.parent1Id === data.parent2Id) {
      setError("Parent 1 and Parent 2 cannot be the same person.");
      return;
    }

    try {
      const familyData = {
        family_name: data.familyName,
        parent1: data.parent1Id,
        max_occupancy: parseInt(data.maxOccupancy),
      };

      if (data.parent2Id) {
        familyData.parent2 = data.parent2Id;
      }

      await createFosterFamily(familyData);
      setSuccess(true);

      if (onSuccess) {
        onSuccess();
      }

      setTimeout(() => {
        onClose();
      }, 1500);
    } catch (error) {
      console.error("Error creating foster family:", error);
      setError("Failed to create foster family.");
    }
  };

  return (
    <Box sx={{ p: 2 }}>
      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          Foster family created successfullly
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
              New Foster Family Information
            </Typography>

            <Grid container spacing={2}>
              <Grid item size={{ xs: 12 }}>
                <Controller
                  name="familyName"
                  control={control}
                  rules={{
                    required: "Family name is required.",
                    minLength: {
                      value: 2,
                      message: "Family name must be at least 2 characters.",
                    },
                  }}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Family Name"
                      fullWidth
                      required
                      error={!!errors.familyName}
                    />
                  )}
                />
              </Grid>

              {/*Parent 1 */}
              <Grid item size={{ xs: 12, sm: 6 }}>
                <Controller
                  name="parent1Id"
                  control={control}
                  rules={{
                    required:
                      "Primary parent is required to create new foster family.",
                  }}
                  render={({ field }) => (
                    <FormControl fullWidth error={!!errors.parent1Id}>
                      <InputLabel>Parent 1</InputLabel>
                      <Select {...field} label="Parent 1 *">
                        {fosterParents.length === 0 ? (
                          <MenuItem disabled>
                            No foster parents available.
                          </MenuItem>
                        ) : (
                          fosterParents.map((parent) => (
                            <MenuItem key={parent.id} value={parent.id}>
                              {parent.last_name}, {parent.first_name}
                            </MenuItem>
                          ))
                        )}
                      </Select>
                      {errors.parent1Id && (
                        <FormHelperText>
                          {errors.parent1Id.message}
                        </FormHelperText>
                      )}
                    </FormControl>
                  )}
                />
              </Grid>

              {/* Parent 2 (Optional) */}
              <Grid item size={{ xs: 12, sm: 6 }}>
                <Controller
                  name="parent2Id"
                  control={control}
                  render={({ field }) => (
                    <FormControl fullWidth error={!!errors.parent2Id}>
                      <InputLabel>Parent 2 (Optional)</InputLabel>
                      <Select {...field} label="Parent 2">
                        <MenuItem value="">
                          <em>None</em>
                        </MenuItem>
                        {fosterParents
                          .filter((parent) => parent.id !== parent1Id)
                          .map((parent) => (
                            <MenuItem key={parent.id} value={parent.id}>
                              {parent.last_name}, {parent.first_name}
                            </MenuItem>
                          ))}
                      </Select>
                    </FormControl>
                  )}
                />
              </Grid>

              {/* Max Occupancy */}
              <Grid item size={{ xs: 12 }}>
                <Controller
                  name="maxOccupancy"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Maximum Occupancy"
                      type="number"
                      fullWidth
                      required
                      error={!!errors.maxOccupancy}
                      helperText={
                        "Maximum number of children this family can house."
                      }
                      slotProps={{ htmlInput: { min: 1, max: 10 } }}
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
