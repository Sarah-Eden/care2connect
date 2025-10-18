import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  List,
  ListItem,
  ListItemText,
  Divider,
  Alert,
} from "@mui/material";
import {
  getUpcomingHealthServiceRecords,
  getOverdueHealthServiceRecords,
} from "../api";

export default function Notifications() {
  const [upcomingServces, setUpcomingServices] = useState([]);
  const [overdueServices, setOverdueServices] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        setError(null);

        const [upcoming, overdue] = await Promise.all([
          getUpcomingHealthServiceRecords(),
          getOverdueHealthServiceRecords(),
        ]);

        console.log("=== NOTIFICATIONS DEBUG ===");
        console.log("Upcoming Services:", upcoming);
        console.log("Overdue services:", overdue);
        console.log("Upcoming count:", upcoming.length);
        console.log("Overdue count:", overdue.length);

        setUpcomingServices(upcoming);
        setOverdueServices(overdue);
      } catch (error) {
        console.error("Error fetching notifications:", error);
        setError("Failed to load notifications");
      }
    };
    fetchNotifications();
  }, []);

  // Function to format HealthsService type for Notification display
  const formatServiceType = (serviceArray) => {
    if (!serviceArray || serviceArray.length === 0) return "Service";

    const services = Array.isArray(serviceArray)
      ? serviceArray
      : [serviceArray];

    return services
      .map((service) => {
        if (service === "well_child") return "Well Child";
        if (service === "dental") return "Dental";
        if (service === "immunization(s)") return "Immunization(s)";
        return service;
      })
      .join(", ");
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      month: "numeric",
      day: "numeric",
      year: "2-digit",
    });
  };

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom textAlign="center">
        Notifications
      </Typography>

      {/* Display error if database get fails */}
      {error !== null && <Alert severity="error">{error}</Alert>}

      {/* Overdue services */}
      {overdueServices.length > 0 && (
        <>
          <Typography
            variant="subtitle1"
            color="error"
            sx={{ fontWeight: "bold", mt: 2, mb: 1 }}
          >
            Past Due
          </Typography>
          <List>
            {overdueServices.map((service) => (
              <>
                <ListItem disablePadding key={service.id}>
                  <ListItemText
                    primary={`${service.child.last_name}, ${service.child.first_name}`}
                    secondary={`Due Date: ${service.due_date}`}
                  />
                </ListItem>
                <Divider />
              </>
            ))}
          </List>
        </>
      )}

      {/* Upcoming Services */}
      {upcomingServces.length > 0 && (
        <>
          <Typography
            variant="subtitle1"
            color="secondary.dark"
            sx={{ fontWeight: "bold", mt: 2, mb: 1 }}
          >
            Upcoming Services
          </Typography>
          <List>
            {upcomingServces.map((service) => (
              <React.Fragment key={service.id}>
                <ListItem disablePadding key={service.id}>
                  <ListItemText
                    primary={`${service.child.last_name}, ${service.child.first_name}`}
                    secondary={
                      <span sx={{ display: "flex", gap: 1, mt: 0.5 }}>
                        <Typography variant="caption">
                          {formatServiceType(service.service)}
                        </Typography>
                        <Typography variant="caption">
                          {formatDate(service.due_date)}
                        </Typography>
                      </span>
                    }
                  />
                </ListItem>
                <Divider />
              </React.Fragment>
            ))}
          </List>
        </>
      )}

      {/* No notifications */}
      {overdueServices.length === 0 && upcomingServces.length === 0 && (
        <Typography
          variant="body2"
          color="text.secondary"
          textAlign="center"
          sx={{ mt: 4 }}
        >
          No upcoming or overdue appointments.
        </Typography>
      )}
    </Box>
  );
}
