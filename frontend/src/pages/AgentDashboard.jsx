import JobForm from "../components/JobForm";
import JobStatus from "../components/JobStatus";
import StepList from "../components/StepList";
import ContextResults from "../components/ContextResults";
import { useAgentJob } from "../hooks/useAgentJob";

export default function AgentDashboard() {
  const { job, error, start } = useAgentJob();

  return (
    <div>
      <JobForm onSubmit={start} />
      {error && <div style={{ color: "red" }}>{error}</div>}
      {job && (
        <>
          <JobStatus job={job} />
          <StepList steps={job.steps} />
          <ContextResults context={job.artifacts?.context_retrieval} />
        </>
      )}
    </div>
  );
}