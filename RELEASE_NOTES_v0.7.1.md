# Release Notes v0.7.1

## 🎉 Major Changes

### Removed Key Transformation Layer
Removed the `_transform_keys_in_data()` function that was lowercasing all API response keys. Models now directly use the MLB Stats API's native `camelCase` format, simplifying the codebase and ensuring accurate representation of API responses.

### Complete Pydantic Migration
This release includes the complete migration from Python dataclasses to Pydantic v2 models across the entire codebase (from v0.7.0). All models now use Pydantic for validation, serialization, and data handling.

**Key Benefits:**
- Automatic data validation with clear error messages
- Built-in serialization with `model_dump()` and `model_dump_json()`
- Pythonic `snake_case` field names while maintaining API `camelCase` compatibility
- Better type safety and IDE support

### Removed Mock Tests
All mock tests and associated JSON fixtures have been removed (22,370+ lines). The test suite now focuses exclusively on external tests that validate against the actual MLB Stats API.

## 📝 Breaking Changes

⚠️ **This is a major version release with breaking changes:**

1. **Field Access**: All model fields now use `snake_case` instead of `camelCase`:
   ```python
   # Before
   game.gamedata.weather
   
   # After
   game.game_data.weather
   ```

2. **Validation Errors**: Invalid data now raises `pydantic.ValidationError` instead of `TypeError`

3. **Serialization**: Use Pydantic methods for serialization:
   ```python
   # New methods
   model.model_dump()
   model.model_dump_json()
   ```

## 🔧 Model Updates

### Core Models
- All models migrated to Pydantic `MLBBaseModel`
- Field aliases updated to match actual API `camelCase` format
- Optional fields properly marked for fields that may be missing

### Specific Model Fixes
- **Game Models**: `gamePk`, `gameData`, `liveData`, `metaData` aliases corrected
- **HomeRunDerby**: `homeRun`, `tieBreaker`, `isHomeRun`, `isTieBreaker` aliases fixed
- **Stats Models**: `wobaCon`, `pitchArsenal` aliases corrected
- **Schedule Models**: `calendarEventId` made optional
- **Standings Models**: `wildcardGamesBack`, `wildcardEliminationNumber` made optional

## 🐛 Bug Fixes

- Fixed missing fields in various stat models
- Added `age` and `caughtstealingpercentage` to `SimplePitchingSplit`
- Fixed `flyballpercentage` field in `AdvancedPitchingSplit`
- Updated models for new MLB API fields
- Fixed missing keys in live feed data

## 📚 Documentation

- Updated README with Pydantic migration examples
- Added "Working with Pydantic Models" section
- Added Contributing section to README
- Updated all code examples to use `snake_case` field names

## 🔄 Migration Guide

If you're upgrading from v0.5.x or v0.6.x:

1. **Update field access**: Change all `camelCase` field names to `snake_case`
   ```python
   # Old
   game.gamedata.weather
   stat.totalsplits
   
   # New
   game.game_data.weather
   stat.total_splits
   ```

2. **Update error handling**: Catch `ValidationError` instead of `TypeError`
   ```python
   from pydantic import ValidationError
   
   try:
       game = Game(**data)
   except ValidationError as e:
       # Handle validation error
   ```

3. **Use Pydantic serialization**: Replace `__dict__` access with `model_dump()`
   ```python
   # Old
   data = game.__dict__
   
   # New
   data = game.model_dump()
   ```

## 📦 Dependencies

- Added `pydantic>=2.0` as a core dependency
- Migrated from setuptools to Poetry for dependency management

## 🧪 Testing

- Removed all mock tests (22,370+ lines)
- External tests updated and passing
- CI/CD pipelines updated to remove mock test runs

## 🙏 Contributors

Thank you to all contributors who helped with this major release!

---

**Full Changelog**: See commit history from v0.5.3 to HEAD
