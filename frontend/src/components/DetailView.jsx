import { useState, useEffect } from "react";
import {
  Box,
  Typography,
  Grid,
  Divider,
  IconButton,
  Card,
  CardContent,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import EditIcon from "@mui/icons-material/Edit";
import NewCaseForm from "./NewCaseForm";
import NewPlacementForm from "./NewPlacementForm";
import NewChildForm from "./NewChildForm";
import NewFosterFamilyForm from "./NewFosterFamily";
import UpdateMedicalForm from "./UpdateMedicalForm";
import UpdateHealthServiceForm from "./UpdateHealthServiceForm";
import {
  getFosterPlacements,
  getFosterFamily,
  getHealthServiceRecords,
  getUser,
} from "../api";

export default function DetailView({
  selectedCase,
  activeForm,
  onCloseForm,
  onCaseCreated,
  onDetailUpdated,
  refresh,
}) {
  const [fosterPlacementDetails, setFosterPlacementDetails] = useState(null);
  const [fosterFamilyDetails, setFosterFamilyDetails] = useState(null);
  const [caseworkerDetails, setCaseworkerDetails] = useState(null);
  const [healthServices, setHealthServices] = useState([]);
  const [editSection, setEditSection] = useState(null);
  const [editingServiceId, setEditingServiceId] = useState(null);
  const [error, setError] = useState(null);

  // Fetch additional data when a case is selected
  useEffect(() => {
    const fetchAdditionalData = async () => {
      if (!selectedCase) {
        setFosterPlacementDetails(null);
        setFosterFamilyDetails(null);
        setCaseworkerDetails(null);
        setHealthServices([]);
        return;
      }

      try {
        const childId = selectedCase.child.id;

        // Fetch caseworker details
        if (selectedCase.caseworker) {
          const caseworker = await getUser(selectedCase.caseworker);
          setCaseworkerDetails(caseworker);
        }

        // Fetch placement
        const allPlacements = await getFosterPlacements();
        const childPlacement = allPlacements.find(
          (p) => p.child === childId && !p.end_date
        );
        setFosterPlacementDetails(childPlacement || null);

        // Fetch foster family if placement exists
        if (childPlacement?.foster_family) {
          const family = await getFosterFamily(childPlacement.foster_family);
          setFosterFamilyDetails(family);
        }

        // Fetch upcoming health service records
        const allHealthServices = await getHealthServiceRecords();
        const childHealthServices = allHealthServices
          .filter((hs) => {
            const hsChildId =
              typeof hs.child === "object" ? hs.child.id : hs.child;
            return (
              Number(hsChildId) === Number(childId) && hs.status === "pending"
            );
          })
          .sort((a, b) => new Date(a.due_date) - new Date(b.due_date));
        setHealthServices(childHealthServices);
      } catch (error) {
        console.error("Error fetching additional data:", error);
        setError("Error fetching child records.");
      }
    };
    fetchAdditionalData();
  }, [selectedCase, refresh]);

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
        {activeForm === "add_case" && (
          <NewCaseForm onClose={onCloseForm} onSuccess={onCaseCreated} />
        )}
        {activeForm === "add_placement" && (
          <NewPlacementForm onClose={onCloseForm} onSuccess={onDetailUpdated} />
        )}
        {activeForm === "add_child" && <NewChildForm onClose={onCloseForm} />}
        {activeForm === "add_foster_family" && (
          <NewFosterFamilyForm onClose={onCloseForm} />
        )}
      </Box>
    );
  }

  {
    /* Show case details for Child selcted from list */
  }
  if (selectedCase) {
    const child = selectedCase.child;

    return (
      <Box sx={{ p: 2 }}>
        {/* Child Header */}
        <Typography variant="h5" color="primary" gutterBottom>
          {child.first_name} {child.last_name}
        </Typography>

        <Divider sx={{ my: 2 }} />

        {/* Basic Information Card */}
        <Card elevation={2} sx={{ mb: 2 }}>
          <CardContent>
            <Typography variant="h6" color="secondary" gutterBottom>
              Basic Information
            </Typography>
            <Grid container spacing={2}>
              <Grid item size={{ xs: 12, sm: 6 }}>
                <Typography variant="subtitle" color="text.secondary">
                  Date of Birth
                </Typography>
                <Typography variant="body1">
                  {new Date(child.dob + "T12:00:00").toLocaleDateString(
                    "en-US"
                  )}
                </Typography>
              </Grid>

              <Grid item size={{ xs: 12, sm: 6 }}>
                <Typography variant="subtitle2" color="text.secondary">
                  Case Status
                </Typography>
                <Chip
                  label={selectedCase.status}
                  color={selectedCase.status === "open" ? "success" : "default"}
                  size="small"
                  sx={{ textTransform: "capitalize" }}
                />
              </Grid>

              <Grid item size={{ xs: 12, sm: 6 }}>
                <Typography variant="subtitle2" color="text.secondary">
                  Case Start Date
                </Typography>
                <Typography variant="body1">
                  {new Date(selectedCase.start_date).toLocaleDateString(
                    "en-US"
                  )}
                </Typography>
              </Grid>

              {caseworkerDetails && (
                <Grid item size={{ xs: 12, sm: 6 }}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Assigned Caseworker
                  </Typography>
                  <Typography variant="body1">
                    {caseworkerDetails.first_name} {caseworkerDetails.last_name}
                  </Typography>
                </Grid>
              )}
            </Grid>
          </CardContent>
        </Card>

        {/* Placement Information Card */}
        <Card elevation={2} sx={{ mb: 2 }}>
          <CardContent>
            <Typography variant="h6" color="secondary" gutterBottom>
              Current Placement
            </Typography>
            {fosterPlacementDetails && fosterFamilyDetails ? (
              <Grid container spacing={2}>
                <Grid item size={{ xs: 12, sm: 6 }}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Foster Family
                  </Typography>
                  <Typography variant="body1">
                    {fosterFamilyDetails.family_name}
                  </Typography>
                </Grid>

                <Grid item size={{ xs: 12, sm: 6 }}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Placement Start Date
                  </Typography>
                  <Typography variant="body1">
                    {new Date(
                      fosterPlacementDetails.start_date
                    ).toLocaleDateString("en-US")}
                  </Typography>
                </Grid>

                <Grid item size={{ xs: 12 }}>
                  <Typography variant="subtitle2" color="text.secondary">
                    Status
                  </Typography>
                  <Chip label="Active" color="success" size="small" />
                </Grid>
              </Grid>
            ) : (
              <Typography variant="body2" color="text.secondary">
                No active placement on record.
              </Typography>
            )}
          </CardContent>
        </Card>

        {/* Medical Information Card */}
        <Card elevation={2} sx={{ mb: 2 }}>
          <CardContent>
            <Box
              sx={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                mb: 2,
              }}
            >
              <Typography variant="h6" color="secondary" gutterBottom>
                Medical Information
              </Typography>
              <IconButton
                size="small"
                onClick={() => setEditSection("medical")}
                color="primary"
              >
                <EditIcon />
              </IconButton>
            </Box>

            {editSection === "medical" ? (
              <UpdateMedicalForm
                child={child}
                onClose={() => setEditSection(null)}
                onSuccess={() => {
                  setEditSection(null);
                  if (onDetailUpdated) onDetailUpdated();
                }}
              />
            ) : (
              <Grid container spacing={2}>
                <Grid item size={{ xs: 12 }}>
                  <Typography
                    variant="subtitle2"
                    color="text.secondary"
                    gutterBottom
                  >
                    Allergies
                  </Typography>
                  <Typography variant="body1">
                    {child.allergies || "None listed"}
                  </Typography>
                </Grid>

                <Grid item size={{ xs: 12 }}>
                  <Typography
                    variant="subtitle2"
                    color="text.secondary"
                    gutterBottom
                  >
                    Medications
                  </Typography>
                  <Typography variant="body1">
                    {child.medications || "None listed"}
                  </Typography>
                </Grid>
              </Grid>
            )}
          </CardContent>
        </Card>

        {/* Upcoming Health Service Card */}
        <Card elevation={2} sx={{ mb: 2 }}>
          <CardContent>
            <Typography variant="h6" color="secondary" gutterBottom>
              Upcoming Health Services
            </Typography>
            {healthServices.length > 0 ? (
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>
                        <strong>Service Type</strong>
                      </TableCell>
                      <TableCell>
                        <strong>Due Date</strong>
                      </TableCell>
                      <TableCell>
                        <strong>Status</strong>
                      </TableCell>
                      <TableCell>
                        <strong>Actions</strong>
                      </TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {healthServices.map((service) => (
                      <TableRow key={service.id}>
                        <TableCell>
                          {Array.isArray(service.service)
                            ? service.service.join(", ")
                            : service.service}
                        </TableCell>
                        <TableCell>
                          {new Date(service.due_date).toLocaleDateString(
                            "en-US"
                          )}
                        </TableCell>
                        <TableCell>
                          <Chip
                            label={service.status}
                            color="warning"
                            size="small"
                            sx={{ textTransform: "capitalize" }}
                          />
                        </TableCell>
                        <TableCell>
                          <IconButton
                            size="small"
                            onClick={() => setEditingServiceId(service.id)}
                            color="primary"
                          >
                            <EditIcon />
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            ) : (
              <Typography variant="body2" color="text.secondary">
                No upcoming health services scheduled.
              </Typography>
            )}
            {editingServiceId && (
              <Box sx={{ mb: 2 }}>
                <UpdateHealthServiceForm
                  healthService={healthServices.find(
                    (s) => s.id === editingServiceId
                  )}
                  onClose={() => setEditingServiceId(null)}
                  onSuccess={() => {
                    setEditingServiceId(null);
                    if (onDetailUpdated) onDetailUpdated();
                  }}
                />
              </Box>
            )}
          </CardContent>
        </Card>
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
