export default function AlphaFoldSection({ structure }) {
  if (!structure) return null;

  const isLink =
    typeof structure === "string" &&
    structure.startsWith("http");

  return (
    <div className="info-row">
      <span className="info-label">🧬 AlphaFold Structure</span>

      {isLink ? (
        <a
          href={structure}
          target="_blank"
          rel="noreferrer"
        >
          🔗 View AlphaFold 3D Structure
        </a>
      ) : (
        <p>{structure}</p>
      )}
    </div>
  );
}
