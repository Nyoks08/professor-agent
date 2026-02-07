export default function JobStatus({ job }) {
  return (
    <div>
      <h3>Status</h3>
      <div><b>Job ID:</b> {job.job_id}</div>
      <div><b>Status:</b> {job.status}</div>
      {job.error && <div style={{ color: "red" }}>{job.error}</div>}
    </div>
  );
}