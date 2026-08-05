"""Shared offline HTTP status matrices and retry-policy assertions.

These status groups document the version 0.8.0 compatibility baseline and are
intended for reuse by later version 0.9.0 strict-mode and retry-policy tests.

They must not contact the live MLB API.
"""

from __future__ import annotations

import pytest
from urllib3.util.retry import Retry


# Final non-404 client errors that currently return an empty MlbResult by
# default rather than raising MlbHttpError. Later strict-mode work should
# reuse this matrix when asserting the opposite behavior.
COMPATIBILITY_CLIENT_ERRORS = (
    400,
    401,
    403,
    405,
    409,
    422,
    429,
)

NOT_FOUND_STATUS = 404

SERVER_ERRORS = (
    500,
    502,
    503,
    504,
)

# Statuses retried by the library-created Session policy.
RETRYABLE_STATUS_CODES = (
    429,
    500,
    502,
    503,
    504,
)

# Ordinary client errors that must not be retried. Includes 404 and the
# non-429 compatibility client errors.
NON_RETRYABLE_CLIENT_ERRORS = (
    400,
    401,
    403,
    404,
    405,
    409,
    422,
)

HTTP_REASON_BY_STATUS = {
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    409: "Conflict",
    422: "Unprocessable Entity",
    429: "Too Many Requests",
    500: "Internal Server Error",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
}


def assert_library_retry_policy(retry: Retry) -> None:
    """Assert the default library retry policy values.

    Kept in tests so retry and contract modules share one assertion helper
    for the public `create_retry_policy()` configuration.
    """
    assert retry.total == 3
    assert retry.connect == 3
    assert retry.read == 2
    assert retry.status == 3
    assert retry.backoff_factor == 0.5
    assert set(retry.status_forcelist) == set(RETRYABLE_STATUS_CODES)
    assert retry.allowed_methods == frozenset({"GET"})
    assert retry.respect_retry_after_header is True
    assert retry.raise_on_status is False
    assert "POST" not in retry.allowed_methods
    assert "PATCH" not in retry.allowed_methods
    assert "DELETE" not in retry.allowed_methods


API_VERSIONS = ("v1", "v1.1")

# Pending version 1.0 default strict HTTP behavior (#284).
XFAIL_PENDING_STRICT_DEFAULT = pytest.mark.xfail(
    strict=True,
    reason="Pending #284: strict HTTP behavior becomes the 1.0 default",
)

# Pending compatibility warning caller location via public Mlb endpoints (#285).
XFAIL_PENDING_WARNING_CALL_SITE = pytest.mark.xfail(
    strict=True,
    reason="Pending #285: compatibility warning must point to the public caller",
)


def adapter_for_api_version(mlb, api_version: str):
    """Return the internal MlbDataAdapter for v1 or v1.1."""
    if api_version == "v1":
        return mlb._mlb_adapter_v1
    if api_version == "v1.1":
        return mlb._mlb_adapter_v1_1
    raise ValueError(f"unsupported api_version: {api_version!r}")


def standalone_adapter_for_version(
    session,
    api_version: str,
    *,
    strict_http: bool = False,
) -> "MlbDataAdapter":
    """Build a versioned MlbDataAdapter sharing a mocked session."""
    from mlbstatsapi import MlbDataAdapter

    return MlbDataAdapter(
        session=session,
        ver=api_version,
        strict_http=strict_http,
    )
