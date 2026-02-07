export default function ContextResults({ context }) {
  if (!context) return null;

  const { faculty = [], grants = [] } = context.results || {};

  return (
    <div>
      <h3>Context Retrieval</h3>

      <h4>Faculty</h4>
      <ol>
        {faculty.map((f, i) => (
          <li key={i}>
            <b>{f.metadata?.doc_id}</b> (score: {f.score})<br />
            <small>{f.snippet}</small>
          </li>
        ))}
      </ol>

      <h4>Grants</h4>
      <ol>
        {grants.map((g, i) => (
          <li key={i}>
            <b>{g.metadata?.doc_id}</b> (score: {g.score})<br />
            <small>{g.snippet}</small>
          </li>
        ))}
      </ol>
    </div>
  );
}