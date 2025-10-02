import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    primary: {
      main: "#3c9a9b",
      light: "#5eb5b6",
      dark: "#2d7778",
      contrastText: "#fff",
    },
    secondary: {
      main: "#e77933",
      light: "#f09a5e",
      dark: "#c05d1f",
      contrastText: "#fff",
    },
    success: {
      main: "#4caf50",
      light: "#6fbf73",
      dark: "#357a38",
      contrastText: "#fff",
    },
    warning: {
      main: "#ffa726",
      light: "#ffb74d",
      dark: "#f57c00",
      contrastText: "#000000",
    },
    error: {
      main: "#ef5350",
      light: "#f44336",
      dark: "#c62828",
      contrastText: "#ffffff",
    },
    info: {
      main: "#42a5f5",
      light: "#64b5f6",
      dark: "#1976d2",
      contrastText: "#ffffff",
    },
    grey: {
      50: "#fafafa",
      100: "#f7f7f7",
      200: "#eeeeee",
      300: "#d1d1d1",
      400: "#bdbdbd",
      500: "#7a7a7a",
      600: "#757575",
      700: "#4a4a4a",
      800: "#424242",
      900: "#2c2c2c",
    },
    text: {
      primary: "#2c2c2c",
      secondary: "#4a4a4a",
      disabled: "#7a7a7a",
    },
    background: {
      default: "#f7f7f7",
      paper: "#ffffff",
    },
  },
  typography: {
    fontFamily: "Roboto, sans-serif",
  },
});

export default theme;
