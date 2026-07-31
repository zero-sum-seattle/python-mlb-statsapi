import sys
from pathlib import Path

# tests/external_tests/... is collected from nested directories that are not packages,
# so the repository root is not always on sys.path by the time a test imports
# tests.alias_audit.
sys.path.insert(0, str(Path(__file__).parent))
