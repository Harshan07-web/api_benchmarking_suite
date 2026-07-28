import { useEffect, useState, useCallback } from "react";
import RunForm from "./components/RunForm";
import ResultView from "./components/ResultView";
import History from "./components/History";
import { runBenchmark, getBenchmark, getAllBenchmarks } from "./api/client";

export default function App() {
  const [runs, setRuns] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(true);
  const [running, setRunning] = useState(false);
  const [activeId, setActiveId] = useState(null);
  const [activeData, setActiveData] = useState(null);
  const [historyError, setHistoryError] = useState(null);

  const loadHistory = useCallback(async () => {
    setLoadingHistory(true);
    setHistoryError(null);
    try {
      const data = await getAllBenchmarks();
      setRuns(data);
    } catch (err) {
      setHistoryError(err.message);
    } finally {
      setLoadingHistory(false);
    }
  }, []);

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  async function handleRun(payload) {
    setRunning(true);
    try {
      const result = await runBenchmark(payload);
      setActiveId(null);
      setActiveData(result);
      loadHistory();
    } finally {
      setRunning(false);
    }
  }

  async function handleSelect(id) {
    setActiveId(id);
    setActiveData(null);
    const data = await getBenchmark(id);
    setActiveData(data);
  }

  return (
    <div className="min-h-screen bg-bg text-text">
      <header className="border-b border-border">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-baseline gap-2">
            <span className="text-accent font-mono text-sm">&#9656;</span>
            <h1 className="text-sm font-medium tracking-wide">benchmark</h1>
          </div>
          <span className="text-[11px] font-mono text-muted">
            HTTP load testing
          </span>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8 grid grid-cols-12 gap-8">
        <aside className="col-span-3 space-y-8">
          <div className="border border-border rounded-sm p-4">
            <h3 className="text-[11px] uppercase tracking-wider text-muted mb-3">
              New run
            </h3>
            <RunForm onRun={handleRun} running={running} />
          </div>

          {historyError ? (
            <p className="text-xs font-mono text-fail px-1">{historyError}</p>
          ) : (
            <History
              runs={runs}
              activeId={activeId}
              onSelect={handleSelect}
              loading={loadingHistory}
            />
          )}
        </aside>

        <section className="col-span-9">
          {!activeData && !running && (
            <div className="h-full min-h-[400px] border border-dashed border-border rounded-sm flex items-center justify-center">
              <p className="text-xs font-mono text-muted">
                Run a benchmark or select one from history.
              </p>
            </div>
          )}
          {running && !activeData && (
            <div className="h-full min-h-[400px] border border-border rounded-sm flex items-center justify-center">
              <p className="text-xs font-mono text-muted animate-pulse">
                sending requests&hellip;
              </p>
            </div>
          )}
          {activeData && (
            <div className="border border-border rounded-sm p-5">
              <ResultView data={activeData} />
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
