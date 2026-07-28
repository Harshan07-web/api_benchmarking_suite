const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail ? JSON.stringify(body.detail) : detail;
    } catch (_) {}
    throw new Error(detail);
  }
  return res.json();
}

export function runBenchmark(payload) {
  return request("/benchmark", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getBenchmark(id) {
  return request(`/benchmark/${id}`);
}

export function getAllBenchmarks() {
  return request(`/benchmark/all`);
}
