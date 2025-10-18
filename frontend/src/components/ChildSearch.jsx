import React, { useState } from "react";
import {
  Box,
  Typography,
  TextField,
  Button,
  Grid,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Card,
  CardContent,
  Alert,
  Divider,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from "@mui/material";
import { getChildren } from "../api";

export default function ChildSearch({
  onSelectChild,
  searchFunction,
  selectedChild,
  onClearSelection,
}) {
  const [searchFirstName, setSearchFirstName] = useState("");
  const [searchLastName, setSearchLastName] = useState("");
  const [searchDOB, setSearchDOB] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    if (!searchFirstName && !searchLastName && !searchDOB) {
      setError("Please enter at least one search criteria.");
      return;
    }

    setError(null);

    try {
      const allChildren = await getChildren();

      const filtered = allChildren.filter((child) => {
        const firstNameMatch = searchFirstName
          ? child.first_name
              .toLowerCase()
              .includes(searchFirstName.toLowerCase())
          : true;
        const lastNameMatch = searchLastName
          ? child.last_name.toLowerCase().includes(searchLastName.toLowerCase())
          : true;
        const dobMatch = searchDOB ? child.dob === searchDOB : true;

        return firstNameMatch && lastNameMatch && dobMatch;
      });

      setSearchResults(filtered);

      if (filtered.length === 0) {
        setError(
          "No children found matching search criteria. Please check input for spelling or date errors."
        );
      }
    } catch (error) {
      console.error("Error searching children:", error);
      setError("Child record search failed.");
    }
  };

  const handleSelectChild = (c) => {
    onSelectChild(c);
    // Clear search results after selection
    setSearchResults([]);
    setSearchFirstName("");
    setSearchLastName("");
    setSearchDOB("");
    setError(null);
  };

  const handleClearSelection = () => {
    onClearSelection();
    setSearchResults([]);
    setError(null);
  };

  // Display selected child on card
  if (selectedChild) {
    return (
      <Card elevation={2} sx={{ mb: 3 }}>
        <CardContent>
          <Box
            sx={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              mb: 2,
            }}
          >
            <Typography variant="h6" color="primary">
              Selected Child
            </Typography>
            <Button
              size="small"
              onClick={handleClearSelection}
              color="secondary"
            >
              Change
            </Button>
          </Box>

          <Typography variant="body1">
            <strong>Name:</strong> {selectedChild.first_name}{" "}
            {selectedChild.last_name}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            <strong>DOB:</strong>{" "}
            {new Date(selectedChild.dob + "T12:00:00").toLocaleDateString(
              "en-US"
            )}
          </Typography>
        </CardContent>
      </Card>
    );
  }

  // Search for child, default on form open
  return (
    <Card elevation={2} sx={{ mb: 3 }}>
      <CardContent>
        <Typography variant="h6" color="primary" gutterBottom>
          Search Child Records
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
            {error}
          </Alert>
        )}

        {/* Search inputs. */}
        <Grid container spacing={2}>
          <Grid item size={{ xs: 12, sm: 4 }}>
            <TextField
              label="First Name"
              value={searchFirstName}
              onChange={(e) => setSearchFirstName(e.target.value)}
              fullWidth
              size="small"
            />
          </Grid>
          <Grid item size={{ xs: 12, sm: 4 }}>
            <TextField
              label="Last Name"
              value={searchLastName}
              onChange={(e) => setSearchLastName(e.target.value)}
              fullWidth
              size="small"
            />
          </Grid>
          <Grid item size={{ xs: 12, sm: 4 }}>
            <TextField
              label="Date of Birth"
              type="date"
              value={searchDOB}
              onChange={(e) => setSearchDOB(e.target.value)}
              fullWidth
              size="small"
              InputLabelProps={{ shrink: true }}
            />
          </Grid>
          <Grid item size={{ xs: 12 }}>
            <Button
              variant="contained"
              color="primary"
              onClick={handleSearch}
              fullWidth
            >
              Search
            </Button>
          </Grid>
        </Grid>

        {/* Search Results */}
        {searchResults.length > 0 && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="subtitle2" gutterBottom>
              Search Results ({searchResults.length} found):
            </Typography>

            {/* Mobile drop down */}
            <Box sx={{ display: { xs: "block", sm: "block", md: "none" } }}>
              <FormControl fullWidth>
                <InputLabel>Select Child</InputLabel>
                <Select
                  value={""}
                  onChange={(e) =>
                    handleSelectChild(
                      searchResults.find((c) => c.id === e.target.value)
                    )
                  }
                >
                  {searchResults.map((c) => (
                    <MenuItem key={c.id} value={c.id}>
                      {c.last_name}, {c.first_name} (DOB:{" "}
                      {new Date(c.dob + "T12:00:00").toLocaleDateString()})
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Box>

            {/* Desktop list */}
            <Box sx={{ display: { xs: "none", sm: "none", md: "block" } }}>
              <List>
                {searchResults.map((c) => (
                  <React.Fragment key={c.id}>
                    <ListItem disablePadding key={c.id}>
                      <ListItemButton
                        onClick={() => handleSelectChild(c)}
                        sx={{
                          "&.Mui-selected": {
                            color: "primary.main",
                            border: "1px solid #bdbdbd",
                          },
                        }}
                      >
                        <ListItemText
                          primary={`${c.last_name}, ${c.first_name}`}
                          secondary={`DOB: ${new Date(
                            c.dob + "T12:00:00"
                          ).toLocaleDateString()}`}
                        />
                      </ListItemButton>
                    </ListItem>
                    <Divider />
                  </React.Fragment>
                ))}
              </List>
            </Box>
          </Box>
        )}
      </CardContent>
    </Card>
  );
}
