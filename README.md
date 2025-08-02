# GitHub Actions Daily Request Example

An example for a friend.

This repository contains a GitHub Actions workflow that runs a Python script daily at midnight to make a GET request to meltingscales.github.io with a Bearer token.

## Files

- `.github/workflows/daily-request.yml` - GitHub Actions workflow configuration
- `scripts/daily_request.py` - Python script that performs the request
- `pyproject.toml` - Project configuration and dependencies (managed by uv)
- `Makefile` - Common development tasks
- `tests/` - Test files

## Setup

### 1. Add the Secret

You need to add a repository secret called `MIKEY_SECRET`:

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `MIKEY_SECRET`
5. Value: Your secret token
6. Click **Add secret**

### 2. Workflow Details

The workflow:
- Runs daily at midnight UTC (`cron: '0 0 * * *'`)
- Can be manually triggered via the GitHub Actions tab
- Uses Ubuntu latest runner
- Sets up Python 3.11
- Installs `uv` for dependency management
- Installs dependencies using `uv sync --no-dev`
- Runs the Python script with the secret as an environment variable
- Uploads the response file as an artifact

### 3. What the Script Does

The Python script (`scripts/daily_request.py`):

1. **Retrieves the secret**: Gets `MIKEY_SECRET` from environment variables
2. **Makes the request**: Sends a GET request to `https://meltingscales.github.io` with the secret as a Bearer token
3. **Saves response**: Saves the complete response (including headers and body) to `response.txt`
4. **Prints output**: Shows a preview of the response in the workflow logs

### 4. Output

- The script creates a `response.txt` file with the complete response
- This file is uploaded as a workflow artifact
- The workflow logs show a preview of the response (first 500 characters)
- You can download the full response file from the Actions tab

## Development

### Local Setup

**Option 1: Using uv (recommended for most systems)**
1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Set up the project**:
   ```bash
   make setup
   ```

3. **Install dependencies**:
   ```bash
   make install-dev
   ```

**Option 2: Using Nix (for NixOS or systems with Nix)**
The Makefile automatically detects if uv is available and falls back to using nix-shell with the required dependencies. No additional setup needed!

### Available Commands

Run `make help` to see all available commands:

- `make setup` - Initial setup with uv
- `make install` - Install production dependencies
- `make install-dev` - Install all dependencies (including dev tools)
- `make run` - Run the script locally (requires MIKEY_SECRET env var)
- `make test` - Run tests
- `make lint` - Run linting checks
- `make format` - Format code with black
- `make clean` - Clean up generated files
- `make check` - Run all checks (lint, format, test)

### Local Testing

To test the script locally:

**Option 1: Set environment variable first**
```bash
export MIKEY_SECRET=your_secret_here
make run
```

**Option 2: Run with secret directly**
```bash
make run-with-secret SECRET=your_secret_here
```

**Option 3: Test with mock secret**
```bash
make test-local
```

## Manual Testing

You can test the workflow manually by:

1. Going to the **Actions** tab in your repository
2. Selecting the "Daily Request Script" workflow
3. Clicking **Run workflow**

## Cron Schedule

The workflow uses the cron expression `0 0 * * *` which means:
- `0` - At minute 0
- `0` - At hour 0 (midnight)
- `*` - Every day of the month
- `*` - Every month
- `*` - Every day of the week

This runs the workflow daily at midnight UTC. 