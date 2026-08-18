import inspect
import warnings
from typing import Protocol

from .exceptions import MlbHttpError
from .warnings import MlbHttpCompatibilityWarning


HTTP_ERROR_BODY_EXCERPT_LIMIT = 500


class _ResponseLike(Protocol):
    content: bytes
    text: str

    def json(self) -> object:
        ...


def _is_mlbstatsapi_module(module_name: str) -> bool:
    """Return True when module_name belongs to this package."""
    return module_name == "mlbstatsapi" or module_name.startswith("mlbstatsapi.")


def _compatibility_warning_stacklevel() -> int:
    """Return a warnings.warn stacklevel for the first non-package caller."""
    frame = inspect.currentframe()
    stacklevel = 1

    try:
        frame = frame.f_back

        while frame is not None:
            module_name = frame.f_globals.get("__name__", "")

            if not _is_mlbstatsapi_module(module_name):
                return stacklevel

            stacklevel += 1
            frame = frame.f_back
    finally:
        del frame

    return 1


def _warn_http_compatibility(
    *,
    status_code: int,
    url: str,
) -> None:
    warnings.warn(
        (
            f"HTTP {status_code} for {url} was suppressed because "
            "strict_http=False explicitly selected compatibility mode, so the "
            "historical empty result was returned. Strict HTTP behavior is the "
            "default in version 1.0. Remove strict_http=False or pass "
            "strict_http=True to raise MlbHttpError."
        ),
        MlbHttpCompatibilityWarning,
        stacklevel=_compatibility_warning_stacklevel(),
    )


def _extract_error_response_data(
    response: _ResponseLike,
) -> dict | list | None:
    """Best-effort JSON extraction from an error response."""
    try:
        if not response.content:
            return None

        data = response.json()
    except Exception:
        return None

    if isinstance(data, (dict, list)):
        return data

    return None


def _extract_error_body_excerpt(
    response: _ResponseLike,
) -> str | None:
    """Best-effort bounded text excerpt from an error response."""
    try:
        if not response.content:
            return None

        text = response.text
    except Exception:
        return None

    if not text:
        return None

    return text[:HTTP_ERROR_BODY_EXCERPT_LIMIT]


def _build_http_error(
    response: _ResponseLike,
    *,
    status_code: int,
    reason: str,
    url: str | None,
    method: str,
) -> MlbHttpError:
    """Build MlbHttpError from transport-neutral response context."""
    try:
        response_data = _extract_error_response_data(response)
    except Exception:
        response_data = None

    try:
        body_excerpt = _extract_error_body_excerpt(response)
    except Exception:
        body_excerpt = None

    return MlbHttpError(
        status_code=status_code,
        reason=reason,
        url=url,
        method=method,
        response_data=response_data,
        body_excerpt=body_excerpt,
    )