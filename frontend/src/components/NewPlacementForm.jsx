import { useState, useEffect } from "react";
import { useForm, Controller } from "react-hook-form";
import {
  Box,
  Typography,
  TextField,
  Button,
  Alert,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Card,
  CardContent,
  FormHelperText,
} from "@mui/material";
import { getChildren, getFosterFamilies, createFosterPlacement } from "../api";
import ChildSearch from "./ChildSearch";

export default function NewPlacementForm({ onClose, onSuccess }) {
  const [selectedChild, setSelectedChild] = useState(null);
  const [fosterFamilies, setFosterFamilies] = useState([]);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const {
    control,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm({
    defaultValues: {
      startDate: new Date().toISOString().split("T")[0],
      fosterFamilyId: "",
      endDate: "",
      endReason: "",
    },
  });

  // Load Foster Families
  useEffect(() => {
    const fetchFosterFamilies = async () => {
      try {
        const families = await getFosterFamilies();
        setFosterFamilies(families);
      } catch (error) {
        console.error("Error fetching foster families:", error);
        setError("Failed to load foster families.");
      }
    };
    fetchFosterFamilies();
  }, []);

  const onSubmit = async (data) => {
    setError(null);
    if (!selectedChild) {
      setError("Please select a child");
      return;
    }

    try {
      const placementData = {
        child: selectedChild.id,
        foster_family: data.fosterFamilyId,
        start_date: data.startDate,
      };

      await createFosterPlacement(placementData);
      setSuccess(true);

      setTimeout(() => {
        onClose();
      }, 1500);
    } catch (error) {
      console.error("Error creating foster placement:", error);
      setError("Failed to create foster placement.");
    }
  };

  return (
    <Box sx={{ p: 2 }}>
      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          Foster Placement created successfully.
        </Alert>
      )}

      <form onSubmit={handleSubmit(onSubmit)}>
        {/* Child Search component */}
        <ChildSearch
          onSelectChild={setSelectedChild}
          searchFunction={getChildren}
          selectedChild={selectedChild}
          onClearSelection={() => setSelectedChild(null)}
        />

        {/* Foster Placement details form */}
        {selectedChild && (
          <Card elevation={2} sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" color="primary" gutterBottom>
                New Foster Placement Details
              </Typography>

              <Grid container spacing={2}>
                <Grid item size={{ xs: 12, sm: 6 }}>
                  <Controller
                    name="fosterFamilyId"
                    control={control}
                    rules={{ required: "Foster Family is required" }}
                    render={({ field }) => (
                      <FormControl fullWidth error={!!errors.fosterFamilyId}>
                        <InputLabel>Foster Family</InputLabel>
                        <Select {...field} label="Foster Family">
                          {fosterFamilies.length === 0 ? (
                            <MenuItem disabled>Loading...</MenuItem>
                          ) : (
                            fosterFamilies.map((family) => (
                              <MenuItem key={family.id} value={family.id}>
                                {family.family_name}
                              </MenuItem>
                            ))
                          )}
                        </Select>
                        {errors.fosterFamilyId && (
                          <FormHelperText>
                            {errors.fosterFamilyId.message}
                          </FormHelperText>
                        )}
                      </FormControl>
                    )}
                  />
                </Grid>

                <Grid item size={{ xs: 12, sm: 6 }}>
                  <Controller
                    name="startDate"
                    control={control}
                    rules={{ required: "Start date is required" }}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        label="Date Placed"
                        type="date"
                        fullWidth
                        required
                        InputLabelProps={{ shrink: true }}
                        error={!!errors.startDate}
                        helperText={errors.startDate?.message}
                      />
                    )}
                  />
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        )}

        {/* Form buttons */}
        {selectedChild && (
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
        )}
      </form>
    </Box>
  );
}
