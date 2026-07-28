function timeAgo(iso) {
  const diff = (Date.now() - new Date(iso).getTime()) / 1000;
  if (diff < 60) return `${Math.floor(diff)}s ago`;
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  return `${Math.floor(diff / 86400)}d ago`;
}

export default function History({ runs, activeId, onSelect, loading }) {
  return (
    <div>
      <h3 className="text-[11px] uppercase tracking-wider text-muted mb-2 px-1">
        History
      </h3>
      {loading && <p className="text-xs font-mono text-muted px-1">loading…</p>}
      {!loading && runs.length === 0 && (
        <p className="text-xs font-mono text-muted px-1">No runs yet.</p>
      )}
      <div className="space-y-1">
        {runs.map((run) => {
          const failed = run.failed_requests > 0;
          const active = run.id === activeId;
          return (
            <button
              key={run.id}
              onClick={() => onSelect(run.id)}
              className={`w-full text-left px-2.5 py-2 rounded-sm border transition-colors ${
                active
                  ? "border-accent bg-accent/5"
                  : "border-transparent hover:border-border hover:bg-surface"
              }`}
            >
              <div className="flex items-center justify-between gap-2">
                <span className="text-xs truncate">
                  {run.benchmark_name || run.url}
                </span>
                <span
                  className={`w-1.5 h-1.5 rounded-full shrink-0 ${
                    failed ? "bg-fail" : "bg-accent"
                  }`}
                />
              </div>
              <div className="flex items-center justify-between mt-0.5">
                <span className="text-[10px] font-mono text-muted">
                  {run.requests_per_second?.toFixed(1)} rps
                </span>
                <span className="text-[10px] font-mono text-muted">
                  {timeAgo(run.created_at)}
                </span>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
