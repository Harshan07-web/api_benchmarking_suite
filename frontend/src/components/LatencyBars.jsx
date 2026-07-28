export default function LatencyBars({ metrics }) {
  const rows = [
    { label: "min", value: metrics.minimum_latency },
    { label: "avg", value: metrics.average_latency },
    { label: "p50", value: metrics.median_latency },
    { label: "p90", value: metrics.p90_latency },
    { label: "p95", value: metrics.p95_latency },
    { label: "p99", value: metrics.p99_latency },
    { label: "max", value: metrics.maximum_latency },
  ];
  const max = Math.max(...rows.map((r) => r.value), 1);

  return (
    <div className="space-y-2">
      {rows.map((r) => (
        <div key={r.label} className="flex items-center gap-3">
          <span className="w-9 text-[11px] font-mono text-muted uppercase">{r.label}</span>
          <div className="flex-1 h-4 bg-border/40 rounded-sm overflow-hidden">
            <div
              className="h-full bg-accent/70"
              style={{ width: `${Math.max((r.value / max) * 100, 2)}%` }}
            />
          </div>
          <span className="w-16 text-right text-[11px] font-mono text-text">
            {r.value.toFixed(1)}ms
          </span>
        </div>
      ))}
    </div>
  );
}
