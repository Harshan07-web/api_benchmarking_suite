function codeColor(code) {
  const n = Number(code);
  if (n >= 200 && n < 300) return "bg-accent/70";
  if (n >= 300 && n < 400) return "bg-yellow-500/70";
  if (n >= 400) return "bg-fail/70";
  return "bg-muted/50";
}

export default function StatusDistribution({ distribution }) {
  const entries = Object.entries(distribution || {});
  if (entries.length === 0) {
    return <p className="text-xs text-muted font-mono">No responses recorded.</p>;
  }
  const total = entries.reduce((sum, [, count]) => sum + count, 0);

  return (
    <div className="space-y-2">
      {entries
        .sort((a, b) => Number(a[0]) - Number(b[0]))
        .map(([code, count]) => (
          <div key={code} className="flex items-center gap-3">
            <span className="w-10 text-[11px] font-mono text-text">{code}</span>
            <div className="flex-1 h-4 bg-border/40 rounded-sm overflow-hidden">
              <div
                className={`h-full ${codeColor(code)}`}
                style={{ width: `${(count / total) * 100}%` }}
              />
            </div>
            <span className="w-14 text-right text-[11px] font-mono text-muted">
              {count} · {((count / total) * 100).toFixed(0)}%
            </span>
          </div>
        ))}
    </div>
  );
}
