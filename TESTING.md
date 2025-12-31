# Quick Test Guide

## What I Fixed

1. **dashboard.py** - Fixed the invalid import syntax
2. **tests/__init__.py** - Created the proper init file
3. **docs/usage.md** - Added complete usage documentation with testing section
4. **cmd_start.py** - Implemented the full start command

## Testing Your Code

### Run All Tests

```bash
pytest
```

### Run Tests with Output

```bash
pytest -v
```

### Run Specific Test File

```bash
pytest tests/test_config.py
pytest tests/test_firefox.py
pytest tests/test_i2pd.py
pytest tests/test_cli.py
```

### Run with Coverage

```bash
# Text output
pytest --cov=i2p_manager

# HTML report (open htmlcov/index.html after)
pytest --cov=i2p_manager --cov-report=html
```

### Test Specific Function

```bash
pytest tests/test_config.py::TestConfigManager::test_default_config
```

## What Tests Do

### test_config.py
- Tests configuration loading/saving
- Tests nested config access
- Tests config merging
- Tests default values

### test_firefox.py
- Tests Firefox profile creation
- Tests profile detection
- Tests proxy configuration
- Uses mocks so it doesn't need real Firefox

### test_i2pd.py
- Tests I2Pd status checking
- Tests daemon control
- Tests HTML parsing
- Uses mocks so it doesn't need real I2Pd

### test_cli.py
- Tests CLI commands
- Tests help messages
- Tests version output

## How to Run Your App Now

```bash
# Format code
black i2p_manager/

# Lint
ruff check i2p_manager/

# Run tests
pytest

# Run the app
i2p-manager

# Or with Python
python -m i2p_manager
```

## Expected Test Results

You should see something like:

```
===== test session starts =====
collected 36 items

tests/test_config.py ............ [ 33%]
tests/test_firefox.py ......... [ 58%]
tests/test_i2pd.py ......... [ 83%]
tests/test_cli.py ...... [100%]

===== 36 passed in 2.34s =====
```

## If Tests Fail

### Mock Issues

Some tests use mocks. If you see errors about mocks, install:

```bash
pip install pytest-mock
```

### Import Errors

If modules can't be found:

```bash
pip install -e .
```

### Module Not Found

Make sure you're in the venv:

```bash
source venv/bin/activate  # macOS/Linux
```

## Next Steps

1. ✅ Run `black i2p_manager/` (should pass now)
2. ✅ Run `ruff check i2p_manager/` (should pass now)
3. ✅ Run `pytest` (should pass with 36 tests)
4. ✅ Run `i2p-manager --help` (should work)
5. 🚀 Start developing!
