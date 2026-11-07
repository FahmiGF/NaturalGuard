"""NATURALGUARD AI — Circuit Breaker & Resilient Ingestion."""
import asyncio
import logging
import time
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger("naturalguard.resilience")


class CircuitBreakerOpenException(Exception):
    pass


class CircuitBreaker:
    def __init__(self, name: str, max_failures: int = 3, reset_timeout: float = 60.0):
        self.name = name
        self.max_failures = max_failures
        self.reset_timeout = reset_timeout
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF-OPEN
        self.last_cached_data: Optional[Any] = None
        self.last_cache_timestamp: Optional[float] = None

    def record_success(self, data: Any):
        self.failure_count = 0
        self.state = "CLOSED"
        self.last_cached_data = data
        self.last_cache_timestamp = time.time()

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.max_failures:
            self.state = "OPEN"
            logger.warning(f"Circuit Breaker for {self.name} is now OPEN after {self.failure_count} failures.")

    def can_attempt(self) -> bool:
        if self.state == "CLOSED":
            return True
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.state = "HALF-OPEN"
                logger.info(f"Circuit Breaker for {self.name} is now HALF-OPEN. Probing...")
                return True
            return False
        if self.state == "HALF-OPEN":
            return True
        return False

    async def call(self, coro_func: Callable, fallback_data: Any = None, timeout_seconds: float = 6.0) -> Dict[str, Any]:
        """Calls coroutine with timeout, retry, and returns payload with data_quality flag."""
        if not self.can_attempt():
            logger.warning(f"Circuit Breaker for {self.name} is OPEN. Serving stale cached data.")
            return {
                "data": self.last_cached_data or fallback_data,
                "data_quality": "stale",
                "source_status": "degraded_cached",
                "circuit_state": self.state
            }

        try:
            result = await asyncio.wait_for(coro_func(), timeout=timeout_seconds)
            self.record_success(result)
            return {
                "data": result,
                "data_quality": "verified",
                "source_status": "online",
                "circuit_state": self.state
            }
        except Exception as exc:
            logger.warning(f"Call to {self.name} failed: {exc}. Recording failure...")
            self.record_failure()
            return {
                "data": self.last_cached_data or fallback_data,
                "data_quality": "stale",
                "source_status": "degraded_cached",
                "circuit_state": self.state,
                "error": str(exc)
            }
