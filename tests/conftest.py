import time
from pathlib import Path
from typing import Callable, Optional

import pytest
import requests

from config import BASE_URL, TIMEOUT_SECONDS, RETRIES

@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture(scope="session")
def http_timeout() -> float:
    return TIMEOUT_SECONDS


@pytest.fixture(scope="session")
def retries() -> int:
    return RETRIES


@pytest.fixture
def session() -> requests.Session:
    """
    requests.Session reutiliza conexiones (keep-alive) y hace los tests más eficientes.
    """
    s = requests.Session()
    yield s
    s.close()


def _is_retryable_exception(exc: Exception) -> bool:
    # Fallas típicas de red (transitorias)
    return isinstance(exc, (requests.Timeout, requests.ConnectionError))


@pytest.fixture
def http_get(session, http_timeout, retries) -> Callable[..., requests.Response]:
    """
    Wrapper simple para GET con timeout + retry suave (sin dependencias extra).
    - retries=1 => máximo 2 intentos total.
    """

    def _get(url: str, *, expected_status: Optional[int] = None) -> requests.Response:
        last_exc: Optional[Exception] = None

        for attempt in range(retries + 1):
            try:
                r = session.get(url, timeout=http_timeout)
                if expected_status is not None:
                    assert r.status_code == expected_status
                return r
            except Exception as exc:
                last_exc = exc
                # Si no es retryable o ya no quedan intentos, fallamos.
                if not _is_retryable_exception(exc) or attempt == retries:
                    raise
                # Backoff mínimo para evitar flakiness por picos de red
                time.sleep(0.3)

        # No debería ocurrir, pero queda explícito:
        assert last_exc is not None
        raise last_exc

    return _get
