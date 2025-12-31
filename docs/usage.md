# Usage Guide

Complete guide to using I2P Easy Manager.

---

## Table of Contents

- [First Time Setup](#first-time-setup)
- [Interactive Dashboard](#interactive-dashboard)
- [Command-Line Interface](#command-line-interface)
- [Configuration](#configuration)
- [I2P Sites](#i2p-sites)
- [Common Workflows](#common-workflows)
- [Tips & Best Practices](#tips--best-practices)

---

## First Time Setup

### 1. Initialize I2P Profile

```bash
i2p-manager init
```

This will:
- Check for Firefox and I2Pd
- Create a dedicated Firefox profile named "i2p-secure"
- Apply Arkenfox privacy hardening
- Configure I2P proxy settings (127.0.0.1:4444)

**Output:**
```
🔧 I2P Easy Manager - Initialization

✓ Dependencies found
✓ Configuration created
✓ Profile created: i2p-secure
✓ Arkenfox settings applied
✓ I2P proxy configured

✓ Initialization complete!

Next steps:
  1. Start I2P: i2p-manager start
  2. Check status: i2p-manager status
  3. Wait 10-30 minutes for I2P network integration
  4. Visit I2P sites (e.g., http://planet.i2p)
```

### 2. Start I2P

```bash
i2p-manager start
```

This will:
- Start the I2Pd daemon
- Launch Firefox with your I2P profile
- Display connection information

**First time?** Wait 10-30 minutes for your router to integrate into the I2P network.

---

## Interactive Dashboard

### Launch Dashboard

```bash
i2p-manager
```

The dashboard shows:
- Real-time connection status
- Number of known peers
- Active tunnels
- Quick action menu

### Dashboard Controls

**Number Keys (1-8):**
- `1` - Start I2P
- `2` - Stop I2P
- `3` - Restart I2P
- `4` - Launch I2P Browser
- `5` - View Configuration
- `6` - View Logs
- `7` - Reset Everything
- `8` - Help & About

**Other Keys:**
- `R` - Refresh status
- `Q` - Quit dashboard

---

## Command-Line Interface

### All Available Commands

```bash
i2p-manager --help
```

### Command Reference

#### `init` - Initialize Profile

```bash
# Basic initialization
i2p-manager init

# Force reinitialize (overwrite existing profile)
i2p-manager init --force
```

#### `start` - Start I2P

```bash
# Start I2Pd and launch Firefox
i2p-manager start

# Start I2Pd only (don't launch Firefox)
i2p-manager start --no-browser
```

#### `stop` - Stop I2P

```bash
# Stop I2Pd daemon
i2p-manager stop
```

#### `status` - Check Status

```bash
# Basic status
i2p-manager status

# Verbose status (shows config paths, etc.)
i2p-manager status --verbose
```

#### `restart` - Restart I2P

```bash
# Restart I2Pd daemon
i2p-manager restart
```

#### `browser` - Launch Browser

```bash
# Launch Firefox with I2P profile
# (I2Pd must already be running)
i2p-manager browser
```

#### `config` - Edit Configuration

```bash
# Open config in default editor
i2p-manager config
```

#### `logs` - View Logs

```bash
# Show last 50 lines
i2p-manager logs

# Show last 100 lines
i2p-manager logs --lines 100

# Follow logs in real-time
i2p-manager logs --follow
```

#### `reset` - Reset Everything

```bash
# Remove profile and config (asks for confirmation)
i2p-manager reset

# Keep I2Pd network data
i2p-manager reset --keep-i2pd-data
```

---

## Configuration

### Config File Location

**macOS/Linux:**
```
~/.config/i2p-manager/config.json
```

**Windows:**
```
%APPDATA%\i2p-manager\config.json
```

### Default Configuration

```json
{
  "i2pd": {
    "host": "127.0.0.1",
    "http_port": 4444,
    "https_port": 4444,
    "socks_port": 4447,
    "console_port": 7070
  },
  "firefox": {
    "profile_name": "i2p-secure",
    "harden_with_arkenfox": true
  },
  "dashboard": {
    "refresh_interval": 5,
    "show_welcome": true
  },
  "version": "0.1.0"
}
```

---

## I2P Sites

### First Connection

**⏳ Be Patient!**

First time connecting to I2P takes 10-30 minutes because:
1. Your router needs to find other I2P routers
2. It builds encrypted tunnels
3. It integrates into the network

**Monitor progress:**
```bash
i2p-manager status
```

Look for:
- **< 10 peers:** Still connecting
- **10-50 peers:** Integrating
- **50+ peers:** Ready to browse!

### Popular I2P Sites

Once connected, try these:

**News & Information:**
- http://planet.i2p - I2P news aggregator
- http://i2pwiki.i2p - I2P wiki

**Community:**
- http://i2pforum.i2p - Main community forum
- http://notbob.i2p - Search engine

**Technical:**
- http://127.0.0.1:7070 - Your router console
- http://stats.i2p - Network statistics

---

## Common Workflows

### Daily Use

```bash
# Morning: Start I2P
i2p-manager start

# Browse I2P sites...

# Evening: Stop I2P
i2p-manager stop
```

### Quick Status Check

```bash
# Dashboard for full view
i2p-manager

# Or quick CLI check
i2p-manager status
```

### Troubleshooting

```bash
# Check status
i2p-manager status -v

# View logs
i2p-manager logs

# Restart if having issues
i2p-manager restart

# Last resort: reset and start fresh
i2p-manager reset
i2p-manager init
i2p-manager start
```

---

## Tips & Best Practices

### Privacy

**Do:**
- ✅ Use only I2P profile for I2P sites
- ✅ Wait for full network integration
- ✅ Check peer count regularly

**Don't:**
- ❌ Use regular Firefox profile for I2P
- ❌ Log into personal accounts in I2P profile
- ❌ Modify I2P profile settings manually

---

## How to Use Tests

### Running Tests

```bash
# Run all tests
pytest

# Run with output
pytest -v

# Run specific test file
pytest tests/test_config.py

# Run with coverage
pytest --cov=i2p_manager

# Generate HTML coverage report
pytest --cov=i2p_manager --cov-report=html
# Then open htmlcov/index.html
```

### Understanding Test Output

```bash
pytest -v
```

Shows:
- ✅ PASSED - Test succeeded
- ❌ FAILED - Test failed (shows why)
- ⚠️ SKIPPED - Test was skipped

### Writing Your Own Tests

Create files in `tests/` starting with `test_`:

```python
# tests/test_example.py
def test_something():
    assert 1 + 1 == 2
```

Then run: `pytest tests/test_example.py`

---

## Getting Help

- [Installation Guide](../docs/installation.md)
- [Development Guide](../docs/development.md)
- [GitHub Issues](https://github.com/yourusername/i2p-easy-manager/issues)
