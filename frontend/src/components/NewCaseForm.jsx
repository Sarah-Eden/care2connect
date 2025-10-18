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
import { getChildren, getUsersByGroup, createCase } from "../api";
import ChildSearch from "./ChildSearch";

export default function NewCaseForm({ onClose, onSuccess }) {
  const [selectedChild, setSelectedChild] = useState(null);
  const [caseworkers, setCaseworkers] = useState(null);
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
      caseworkerId: "",
      status: "open",
    },
  });

  // Load caseworkers
  useEffect(() => {
    const fetchCaseworkers = async () => {
      try {
        const caseworkerUsers = await getUsersByGroup("Caseworker");
        setCaseworkers(caseworkerUsers);
      } catch (error) {
        console.error("Error fetching caseworkers:", error);
        setError("Failed to load caseworkers.");
      }
    };
    fetchCaseworkers();
  }, []);

  const onSubmit = async (data) => {
    setError(null);

    if (!selectedChild) {
      setError("Please select a child");
      return;
    }

    try {
      const caseData = {
        child: selectedChild.id,
        caseworker: data.caseworkerId,
        start_date: data.startDate,
        status: data.status,
      };

      await createCase(caseData);
      setSuccess(true);

      setTimeout(() => {
        onClose();
      }, 1500);
    } catch (error) {
      console.error("Error creating case:", error);
      setError("Failed to create case.");
    }
  };

  return (
    <Box sx={{ p: 2 }}>
      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          Case created successfully.
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

        {/* Case details form */}
        {selectedChild && (
          <Card elevation={2} sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" color="primary" gutterBottom>
                New Case Details
              </Typography>

              <Grid container spacing={2}>
                <Grid item size={{ xs: 12, sm: 6 }}>
                  <Controller
                    name="startDate"
                    control={control}
                    rules={{ required: "Start date is required" }}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        label="Date Opened"
                        type="date"
                        fullWidth
                        required
                        slotProps={{ inputLabel: { shrink: true } }}
                        error={!!errors.startDate}
                        helperText={errors.startDate?.message}
                      />
                    )}
                  />
                </Grid>

                <Grid item size={{ xs: 12, sm: 6 }}>
                  <Controller
                    name="status"
                    control={control}
                    rules={{ required: "Status is required" }}
                    render={({ field }) => (
                      <FormControl fullWidth error={!!errors.status}>
                        <InputLabel>Status</InputLabel>
                        <Select {...field} label="Status">
                          <MenuItem value="open">Open</MenuItem>
                          <MenuItem value="closed">Closed</MenuItem>
                        </Select>
                        {errors.status && (
                          <FormHelperText>
                            {errors.status.message}
                          </FormHelperText>
                        )}
                      </FormControl>
                    )}
                  />
                </Grid>

                <Grid item size={{ xs: 12 }}>
                  <Controller
                    name="caseworkerId"
                    control={control}
                    rules={{ required: "Caseworker is required" }}
                    render={({ field }) => (
                      <FormControl fullWidth error={!!errors.caseworkerId}>
                        <InputLabel>Caseworker</InputLabel>
                        <Select {...field} label="Caseworker">
                          {caseworkers.length === 0 ? (
                            <MenuItem disabled>Loading...</MenuItem>
                          ) : (
                            caseworkers.map((cw) => (
                              <MenuItem key={cw.id} value={cw.id}>
                                {cw.last_name}, {cw.first_name}
                              </MenuItem>
                            ))
                          )}
                        </Select>
                        {errors.caseworkerId && (
                          <FormHelperText>
                            {errors.caseworkerId.message}
                          </FormHelperText>
                        )}
                      </FormControl>
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
