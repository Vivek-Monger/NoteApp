# GitHub Actions Workflows

This directory contains CI/CD workflows for the NoteApp project.

## Workflows

### `ci.yml`

Main Continuous Integration workflow that runs on every push and pull request to `main` or `master` branch.

**What it does:**
- Runs Python tests with multiple Python versions (3.10, 3.11)
- Lints code with flake8
- Builds Docker image
- Tests Docker container startup
- Scans for security vulnerabilities
- Optionally pushes to Docker Hub

**How to use:**
1. Push code to GitHub
2. CI runs automatically
3. Check results in the **Actions** tab

**Configuration:**
- No action needed - works out of the box
- Optional: Add Docker Hub secrets for automatic image pushes

See [CI_SETUP.md](../CI_SETUP.md) for detailed documentation.

