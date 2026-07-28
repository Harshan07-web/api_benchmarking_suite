import { useState } from "react";
import Stat from "./Stat";
import LatencyBars from "./LatencyBars";
import StatusDistribution from "./StatusDistribution";

// Normalizes either the full POST /benchmark response, or a flat
// BenchmarkRun row from GET /benchmark/{id}, into one shape.
function normalize(data) {
  if (data.benchmark && data.metrics) {
    return {
      name: data.benchmark.benchmark_name,
      url: data.benchmark.url,
      method: data.benchmark.method,
      total_requests: data.benchmark.total_requests,
      concurrency: data.benchmark.concurrency,
      duration_ms: data.benchmark.duration_ms,
      requests_per_second: data.benchmark.requests_per_second,
      metrics: data.metrics,
      distribution: data.response_distribution,
      results: data.results,
    };
  }
  return {
    name: data.benchmark_name,
    url: data.url,
    method: data.http_method,
    total_requests: data.total_requests,
    concurrency: data.concurrency,
    duration_ms: data.duration_ms,
    requests_per_second: data.requests_per_second,
    metrics: {
      successful_requests: data.successful_requests,
      failed_requests: data.failed_requests,
      success_rate: data.success_rate,
      failure_rate: data.failure_rate,
      average_latency: data.average_latency,
      median_latency: data.median_latency,
      p90_latency: data.p90_latency,
      p95_latency: data.p95_latency,
      p99_latency: data.p99_latency,
      minimum_latency: data.minimum_latency,
      maximum_latency: data.maximum_latency,
    },
    distribution: null,
    results: null,
  };
}

export default function ResultView({ data }) {
  const [showAll, setShowAll] = useState(false);
  if (!data) return null;

  const r = normalize(data);
  const m = r.metrics;
  const rows = r.results || [];
  const visibleRows = showAll ? rows : rows.slice(0, 25);

  return (
    <div className="space-y-6">
      <div>
        <div className="flex items-center gap-2 mb-1">
          <span className="text-[11px] font-mono px-1.5 py-0.5 border border-border rounded-sm text-muted">
            {r.method}
          </span>
          <h2 className="text-sm font-medium truncate">{r.name || "Unnamed run"}</h2>
        </div>
        <p className="text-xs font-mono text-muted truncate">{r.url}</p>
      </div>

      <div className="grid grid-cols-4 gap-2">
        <Stat label="RPS" value={r.requests_per_second} />
        <Stat label="Duration" value={r.duration_ms} unit="ms" />
        <Stat
          label="Success"
          tone="accent"
          value={`${m.successful_requests}/${r.total_requests}`}
        />
        <Stat
          label="Failed"
          tone={m.failed_requests > 0 ? "fail" : undefined}
          value={m.failed_requests}
        />
      </div>

      <div>
        <h3 className="text-[11px] uppercase tracking-wider text-muted mb-2">Latency</h3>
        <LatencyBars metrics={m} />
      </div>

      {r.distribution && (
        <div>
          <h3 className="text-[11px] uppercase tracking-wider text-muted mb-2">
            Response codes
          </h3>
          <StatusDistribution distribution={r.distribution} />
        </div>
      )}

      {rows.length > 0 && (
        <div>
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-[11px] uppercase tracking-wider text-muted">
              Requests ({rows.length})
            </h3>
            {rows.length > 25 && (
              <button
                onClick={() => setShowAll((s) => !s)}
                className="text-[11px] font-mono text-accent hover:underline"
              >
                {showAll ? "show less" : "show all"}
              </button>
            )}
          </div>
          <div className="border border-border rounded-sm max-h-80 overflow-y-auto">
            <table className="w-full text-[11px] font-mono">
              <thead className="sticky top-0 bg-surface">
                <tr className="text-muted border-b border-border">
                  <th className="text-left font-normal px-3 py-1.5">#</th>
                  <th className="text-left font-normal px-3 py-1.5">status</th>
                  <th className="text-left font-normal px-3 py-1.5">latency</th>
                  <th className="text-left font-normal px-3 py-1.5">error</th>
                </tr>
              </thead>
              <tbody>
                {visibleRows.map((row, i) => (
                  <tr key={i} className="border-b border-border/50 last:border-0">
                    <td className="px-3 py-1 text-muted">{i + 1}</td>
                    <td
                      className={`px-3 py-1 ${
                        row.success ? "text-accent" : "text-fail"
                      }`}
                    >
                      {row.status_code ?? "—"}
                    </td>
                    <td className="px-3 py-1">
                      {row.latency_ms != null ? `${row.latency_ms.toFixed(1)}ms` : "—"}
                    </td>
                    <td className="px-3 py-1 text-muted truncate max-w-[200px]">
                      {row.error || ""}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
