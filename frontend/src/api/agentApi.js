export async function startAgentJob(payload) {
  const res = await fetch("/api/agentic_workflow_async", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to start job");
  return res.json();
}

export async function getAgentJobStatus(jobId) {
  const res = await fetch(`/api/agentic_workflow_status/${jobId}`);
  if (!res.ok) throw new Error("Failed to fetch job status");
  return res.json();
}