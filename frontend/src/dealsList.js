import React from "react";
import { createRoot } from "react-dom/client";
import AppDealsList from "./sections/AppDealsList";

const root = createRoot(document.getElementById("app"));
root.render(<AppDealsList />);
