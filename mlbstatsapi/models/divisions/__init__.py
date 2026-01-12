from .division import Division
from mlbstatsapi.models.leagues import League

# Rebuild to resolve forward reference to League
Division.model_rebuild()