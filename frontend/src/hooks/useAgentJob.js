import { useEffect, useState } from "react";
import { startAgentJob, getAgentJobStatus } from "../api/agentApi";

export function useAgentJob() {
  const [job, setJob] = useState(null);
  const [error, setError] = useState(null);

  const start = async (payload) => {
    setError(null);
    const data = await startAgentJob(payload);
    setJob(data);
  };

  useEffect(() => {
    if (!job?.job_id) return;

    const interval = setInterval(async () => {
      try {
        const data = await getAgentJobStatus(job.job_id);
        setJob(data);
        if (["done", "failed"].includes(data.status)) {
          clearInterval(interval);
        }
      } catch (e) {
        setError(e.message);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [job?.job_id]);

  return { job, error, start };
}