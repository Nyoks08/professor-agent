export default function StepList({ steps }) {
  return (
    <div>
      <h3>Steps</h3>
      <ul>
        {steps.map((s) => (
          <li key={s.name}>
            <b>{s.name}</b> — {s.status}
            {s.message && ` (${s.message})`}
          </li>
        ))}
      </ul>
    </div>
  );
}