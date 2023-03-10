import React from "react";
import { createRoot } from "react-dom/client";
import AppOwners from "./sections/AppOwners";

const root = createRoot(document.getElementById("app"));
root.render(<AppOwners />);
