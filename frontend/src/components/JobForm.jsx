import { useState } from "react";

export default function JobForm({ onSubmit }) {
  const [goal, setGoal] = useState("Hospital readmission prediction using ML");
  const [projectIdea, setProjectIdea] = useState(
    "Predict 30-day readmission using structured EHR data"
  );
  const [profileText, setProfileText] = useState(
    "MS Data Analytics student focusing on ML systems"
  );

  return (
    <div>
      <h2>Start Agent Workflow</h2>

      <input value={goal} onChange={(e) => setGoal(e.target.value)} />
      <input value={projectIdea} onChange={(e) => setProjectIdea(e.target.value)} />
      <input value={profileText} onChange={(e) => setProfileText(e.target.value)} />

      <button
        onClick={() =>
          onSubmit({
            goal,
            project_idea: projectIdea,
            profile_text: profileText,
          })
        }
      >
        Start
      </button>
    </div>
  );
}