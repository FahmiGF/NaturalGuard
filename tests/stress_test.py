"""NATURALGUARD AI — High-Concurrency Stress Test & Robustness Fuzzing Suite."""
import sys
import time
import random
import statistics
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add backend directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent / "backend"))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

ENDPOINTS = [
    ("GET", "/api/v1/disasters", None),
    ("GET", "/api/v1/alerts", None),
    ("GET", "/api/v1/forecast", None),
    ("GET", "/api/v1/risk-map", None),
    ("GET", "/api/v1/hazard/flood", None),
    ("GET", "/api/v1/hazard/volcano", None),
    ("GET", "/api/v1/hazard/earthquake", None),
    ("GET", "/api/v1/data-sources", None),
    ("GET", "/api/v1/evaluation/metrics", None),
    ("GET", "/api/v1/evaluation/prediction-vs-actual", None),
    ("GET", "/api/v1/correlation", None),
    ("GET", "/api/v1/copilot/voice-script", None),
    ("POST", "/api/v1/copilot/chat", {"question": "Bagaimana risiko banjir di Bekasi?"}),
    ("POST", "/api/v1/copilot/chat", {"question": "Status aktivitas Semeru?"}),
    ("POST", "/api/v1/copilot/chat", {"question": "Info gempa bumi terkini?"}),
]

FUZZ_PARAMS = [
    {"hazard": "flood", "min_risk": 50.0},
    {"hazard": "volcano", "province": "Jawa Timur"},
    {"hazard": "nonexistent_hazard_type_999"},  # Edge case: unknown hazard
    {"min_risk": -100.0},                       # Edge case: negative risk
    {"min_risk": 99999.0},                      # Edge case: very high risk
    {"province": "' OR 1=1 --"},                # Security fuzz: SQL injection string
    {"province": "<script>alert('xss')</script>"},# Security fuzz: XSS payload
    {"status": "all"},
    {"is_official": "true"},
    {"is_official": "false"},
]


def execute_single_request(req_id: int):
    """Executes a single test request with latency measurement."""
    # Mix normal endpoints and fuzzed queries
    method, path, body = random.choice(ENDPOINTS)
    fuzz = random.choice(FUZZ_PARAMS)

    start = time.perf_counter()
    try:
        if method == "GET":
            # 50% chance to append fuzz parameters
            params = fuzz if random.random() > 0.5 else None
            resp = client.get(path, params=params)
        else:
            resp = client.post(path, json=body)

        latency_ms = (time.perf_counter() - start) * 1000.0
        success = (resp.status_code == 200)

        return {
            "req_id": req_id,
            "status_code": resp.status_code,
            "latency_ms": latency_ms,
            "success": success,
            "path": path
        }
    except Exception as exc:
        latency_ms = (time.perf_counter() - start) * 1000.0
        return {
            "req_id": req_id,
            "status_code": 500,
            "latency_ms": latency_ms,
            "success": False,
            "error": str(exc),
            "path": path
        }


def run_stress_test(total_requests: int = 1000, max_workers: int = 25):
    print("=" * 65)
    print(" 🚀 NATURALGUARD AI — HIGH CONCURRENCY STRESS & FUZZING TEST")
    print(f" Total Requests: {total_requests} | Concurrency Workers: {max_workers}")
    print("=" * 65)

    start_total = time.perf_counter()
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(execute_single_request, i) for i in range(total_requests)]
        for f in as_completed(futures):
            results.append(f.result())

    total_time = time.perf_counter() - start_total
    latencies = [r["latency_ms"] for r in results]
    successes = [r for r in results if r["success"]]
    failures = [r for r in results if not r["success"]]

    latencies.sort()
    p50 = statistics.median(latencies)
    p95 = latencies[int(len(latencies) * 0.95)]
    p99 = latencies[int(len(latencies) * 0.99)]
    avg_latency = statistics.mean(latencies)
    rps = total_requests / total_time

    print(f"\n[RESULTS SUMMARY]")
    print(f" • Total Completed : {len(results)} requests")
    print(f" • Successful (200): {len(successes)} ({len(successes)/len(results)*100:.1f}%)")
    print(f" • Failed          : {len(failures)}")
    print(f" • Total Time Taken: {total_time:.3f} seconds")
    print(f" • Throughput      : {rps:.1f} requests/sec (RPS)")
    print(f"\n[LATENCY DISTRIBUTION]")
    print(f" • Min Latency     : {min(latencies):.2f} ms")
    print(f" • Mean Latency    : {avg_latency:.2f} ms")
    print(f" • Median (P50)    : {p50:.2f} ms")
    print(f" • P95 Latency     : {p95:.2f} ms")
    print(f" • P99 Latency     : {p99:.2f} ms")
    print(f" • Max Latency     : {max(latencies):.2f} ms")
    print("=" * 65)

    if failures:
        print(f"⚠️ Warning: {len(failures)} requests failed! Details:")
        for fail in failures[:5]:
            print("  ", fail)
        sys.exit(1)
    else:
        print("✅ STRESS & ROBUSTNESS TEST PASSED: 100% SUCCESS WITH ZERO FAILURES!")


if __name__ == "__main__":
    run_stress_test(total_requests=1000, max_workers=25)
