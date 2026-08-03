"""Package warning categories.

Kept in a dedicated module so callers can filter package warnings by class
without importing the HTTP adapter internals.
"""


class MlbHttpCompatibilityWarning(FutureWarning):
    """A compatibility-mode HTTP response that strict mode would raise.

    FutureWarning is used instead of DeprecationWarning because this notice is
    aimed at application users and must stay visible under default filters.
    """
