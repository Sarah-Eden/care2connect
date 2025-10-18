import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  List,
  ListItem,
  ListItemText,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  ListItemButton,
  Divider,
  Alert,
} from "@mui/material";
import { getCases } from "../api";

export default function CaseList({ onSelect, refresh }) {
  const [cases, setCases] = useState([]);
  const [filter, setFilter] = useState("");
  const [selectedId, setSelectedId] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCases = async () => {
      try {
        setError(null);
        const data = await getCases();
        setCases(data);
      } catch (error) {
        console.error("Error fetching cases:", error);
        setError("Failed to load cases.");
      }
    };
    fetchCases();
  }, [refresh]);

  const filteredCases = cases.filter((c) =>
    `${c.child.first_name} ${c.child.last_name}`
      .toLowerCase()
      .includes(filter.toLowerCase())
  );

  const handleSelect = (c) => {
    setSelectedId(c.id);
    onSelect(c);
  };

  return (
    <Box sx={{ p: { xs: 1, sm: 2, textAlign: "center" } }}>
      <Typography variant="h6">Assigned Cases</Typography>

      {/* Mobile drop down */}
      <Box sx={{ display: { xs: "block", sm: "block", md: "none" } }}>
        <FormControl fullWidth>
          <InputLabel>Select Case</InputLabel>
          <Select
            value={selectedId || ""}
            onChange={(e) =>
              handleSelect(filteredCases.find((c) => c.id === e.target.value))
            }
          >
            {filteredCases.map((c) => (
              <MenuItem key={c.id} value={c.id}>
                {c.child.last_name}, {c.child.first_name} (Status: {c.status})
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      {/* Desktop list */}
      <Box sx={{ display: { xs: "none", sm: "none", md: "block" } }}>
        <TextField
          label="Filter"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          fullWidth
          margin="normal"
        />
        <List>
          {filteredCases.map((c) => (
            <React.Fragment key={c.id}>
              <ListItem disablePadding key={c.id}>
                <ListItemButton
                  selected={selectedId === c.id}
                  onClick={() => handleSelect(c)}
                  sx={{
                    "&.Mui-selected": {
                      color: "primary.main",
                      border: "1px solid #bdbdbd",
                    },
                  }}
                >
                  <ListItemText
                    primary={`${c.child.last_name}, ${c.child.first_name}`}
                    secondary={`Status: ${c.status}`}
                  />
                </ListItemButton>
              </ListItem>
              <Divider />
            </React.Fragment>
          ))}
        </List>
      </Box>
      {filteredCases.length === 0 && <Typography>No cases found.</Typography>}
    </Box>
  );
}
