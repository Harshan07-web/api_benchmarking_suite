export default function Stat({ label, value, unit, tone }) {
  const toneCls =
    tone === "accent" ? "text-accent" : tone === "fail" ? "text-fail" : "text-text";
  return (
    <div className="border border-border rounded-sm px-3 py-2.5">
      <div className="text-[11px] uppercase tracking-wider text-muted mb-1">{label}</div>
      <div className={`font-mono text-lg leading-none ${toneCls}`}>
        {value}
        {unit && <span className="text-xs text-muted ml-1">{unit}</span>}
      </div>
    </div>
  );
}
