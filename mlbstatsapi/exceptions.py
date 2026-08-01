class TheMlbStatsApiException(Exception):
    pass


class MlbTransportError(TheMlbStatsApiException):
    """A network or request transport failure."""


class MlbTimeoutError(MlbTransportError):
    """A connection or read timeout."""


class MlbHttpError(TheMlbStatsApiException):
    """An unexpected HTTP response."""

    def __init__(
        self,
        status_code: int,
        reason: str,
        url: str | None = None,
    ):
        self.status_code = int(status_code)
        self.reason = str(reason)
        self.url = url

        super().__init__(
            f"{self.status_code}: {self.reason}"
        )


class MlbDecodeError(TheMlbStatsApiException):
    """A successful response contained invalid JSON."""
