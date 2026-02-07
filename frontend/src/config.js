// frontend/src/config.js

// How often the frontend polls job status (ms)
export const POLL_INTERVAL_MS = 1000;

// Default values for the agent form
export const DEFAULT_AGENT_PAYLOAD = {
  goal: "Hospital readmission prediction using ML",
  project_idea: "Predict 30-day readmission using structured EHR data",
  profile_text: "MS Data Analytics student focusing on ML systems",
};

// Limits / UI behavior
export const MAX_CONTEXT_RESULTS = 5;

// App metadata (nice for headers / titles later)
export const APP_NAME = "Professor Agent";