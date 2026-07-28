import { useState } from "react";

const DEFAULTS = {
  benchmark_name: "",
  url: "",
  method: "GET",
  total_requests: 100,
  concurrency: 10,
  timeout: 15,
};

function Field({ label, hint, children }) {
  return (
    <label className="block">
      <div className="flex items-baseline justify-between mb-1.5">
        <span className="text-[11px] uppercase tracking-wider text-muted">{label}</span>
        {hint && <span className="text-[11px] text-muted/60 font-mono">{hint}</span>}
      </div>
      {children}
    </label>
  );
}

const inputBaseCls =
  "bg-bg border border-border rounded-sm px-3 py-2 text-sm font-mono text-text placeholder:text-muted/50 focus:outline-none focus:border-accent transition-colors";

const inputCls = `w-full ${inputBaseCls}`;

export default function RunForm({ onRun, running }) {
  const [form, setForm] = useState(DEFAULTS);
  const [error, setError] = useState(null);

  function update(key, value) {
    setForm((f) => ({ ...f, [key]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    if (!form.url) {
      setError("URL is required.");
      return;
    }
    try {
      await onRun({
        benchmark_name: form.benchmark_name || null,
        url: form.url,
        method: form.method,
        total_requests: Number(form.total_requests),
        concurrency: Number(form.concurrency),
        timeout: Number(form.timeout),
      });
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Field label="Target URL">
        <div className="flex gap-2">
          <select
            value={form.method}
            onChange={(e) => update("method", e.target.value)}
            className={`${inputBaseCls} w-24 shrink-0 cursor-pointer`}
          >
            <option>GET</option>
            <option>POST</option>
          </select>
          <input
            type="text"
            placeholder="https://api.example.com/endpoint"
            value={form.url}
            onChange={(e) => update("url", e.target.value)}
            className={`${inputBaseCls} flex-1 min-w-0`}
          />
        </div>
      </Field>

      <Field label="Run name" hint="optional">
        <input
          type="text"
          placeholder="e.g. checkout-endpoint-v2"
          value={form.benchmark_name}
          onChange={(e) => update("benchmark_name", e.target.value)}
          className={inputCls}
        />
      </Field>

      <div className="grid grid-cols-3 gap-3">
        <Field label="Requests">
          <input
            type="number"
            min={1}
            value={form.total_requests}
            onChange={(e) => update("total_requests", e.target.value)}
            className={inputCls}
          />
        </Field>
        <Field label="Concurrency">
          <input
            type="number"
            min={1}
            value={form.concurrency}
            onChange={(e) => update("concurrency", e.target.value)}
            className={inputCls}
          />
        </Field>
        <Field label="Timeout" hint="sec">
          <input
            type="number"
            min={1}
            value={form.timeout}
            onChange={(e) => update("timeout", e.target.value)}
            className={inputCls}
          />
        </Field>
      </div>

      {error && (
        <div className="text-xs font-mono text-fail border border-fail/30 bg-fail/5 rounded-sm px-3 py-2">
          {error}
        </div>
      )}

      <button
        type="submit"
        disabled={running}
        className="w-full bg-accent text-bg font-medium text-sm rounded-sm py-2.5 hover:bg-accent/90 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
      >
        {running ? "Running…" : "Run benchmark"}
      </button>
    </form>
  );
}