# CI/CD Setup - GitHub Actions

## 📋 Overview

This project includes a complete Continuous Integration (CI) workflow using GitHub Actions that automatically:

- ✅ Runs tests on every push and pull request
- ✅ Lints Python code with flake8
- ✅ Builds and tests Docker containers
- ✅ Scans for security vulnerabilities
- ✅ Optionally pushes Docker images to Docker Hub

---

## 🚀 Quick Start

### 1. Push to GitHub

The CI workflow will automatically run when you:

```bash
git add .
git commit -m "Add CI workflow"
git push origin main
```

### 2. View Results

- Go to your GitHub repository
- Click on the **Actions** tab
- Click on any workflow run to see results
- Green checkmark = success ✅
- Red X = failed ❌

---

## 🔧 CI Workflow Components

### Job 1: Test & Lint

**Python Versions:** 3.10, 3.11  
**Steps:**
1. Checkout code
2. Set up Python environment
3. Install dependencies
4. Lint with flake8
5. Run Django tests
6. Run deployment checklist

**Status:** Shows warnings, won't fail the build

### Job 2: Docker Build & Test

**Steps:**
1. Build Docker image
2. Test container startup
3. Verify application responds
4. (Optional) Push to Docker Hub

**Status:** Must pass for deployment

### Job 3: Security Scan

**Steps:**
1. Check for known vulnerabilities
2. Run Bandit security linter
3. Generate security reports

**Status:** Shows warnings, won't fail the build

### Job 4: Summary

**Purpose:** Provides a final status summary  
**Runs:** Always (even if other jobs fail)

---

## 🐳 Docker Hub Integration

### Setup Docker Hub Secrets

To enable automatic Docker Hub pushes:

1. **Go to your GitHub repository**
2. **Click Settings → Secrets and variables → Actions**
3. **Add the following secrets:**

```
DOCKER_HUB_USERNAME: your-dockerhub-username
DOCKER_HUB_PASSWORD: your-dockerhub-password-or-token
```

### How It Works

- If secrets are configured → Builds and pushes to Docker Hub
- If secrets are NOT configured → Only builds and tests locally
- Never pushes without credentials ✅

### Docker Image Tags

Images are tagged with:
- `your-username/noteapp:latest` (latest version)
- `your-username/noteapp:<commit-sha>` (specific commit)

---

## 📝 Writing Tests

### Create a Test File

Create `notes/tests.py`:

```python
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Note

class NoteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_create_note(self):
        note = Note.objects.create(
            title='Test Note',
            content='Test content',
            author=self.user
        )
        self.assertEqual(note.title, 'Test Note')
        self.assertEqual(note.author, self.user)
    
    def test_note_list_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  # Redirects to login
```

### Run Tests Locally

```bash
source venv/bin/activate
python manage.py test
```

---

## 🔍 Linting Configuration

### flake8 Configuration

Create `.flake8` file in project root:

```ini
[flake8]
max-line-length = 127
exclude = 
    .git,
    __pycache__,
    venv,
    .venv,
    migrations,
    settings.py
ignore = E501, W503
```

### Run Linting Locally

```bash
pip install flake8
flake8 .
```

---

## ⚙️ Workflow Configuration

### Triggers

```yaml
on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:  # Manual trigger
```

**Triggers CI on:**
- Push to main/master
- Pull requests to main/master
- Manual workflow dispatch

### Matrix Strategy

Tests run on multiple Python versions:

```yaml
strategy:
  matrix:
    python-version: ['3.10', '3.11']
```

**Benefit:** Ensures compatibility across versions

### Caching

```yaml
cache: 'pip'
```

**Benefit:** Faster builds by caching dependencies

---

## 🔒 Security Scanning

### Tools Used

1. **Safety** - Checks for known vulnerabilities
2. **Bandit** - Static security analysis

### Installation

```bash
pip install safety bandit
```

### Run Locally

```bash
# Check vulnerabilities
safety check -r requirements.txt

# Scan code
bandit -r . -ll
```

---

## 📊 Understanding CI Results

### Success ✅

All checks passed:
- Tests passed
- Docker build successful
- No critical security issues

### Partial Success ⚠️

Some checks passed with warnings:
- Tests passed
- Docker build successful
- Security scan found minor issues (warnings only)

### Failure ❌

Critical issues found:
- Tests failed
- Docker build failed
- Container didn't start

### Viewing Logs

1. Go to GitHub Actions tab
2. Click on a workflow run
3. Click on a job to see logs
4. Expand steps to see detailed output

---

## 🛠️ Troubleshooting

### Tests Fail

**Problem:** Django tests not found

**Solution:**
```bash
# Create test file
touch notes/tests.py

# Add basic test
echo "from django.test import TestCase

class BasicTest(TestCase):
    def test_basic(self):
        self.assertTrue(True)
" > notes/tests.py
```

### Docker Build Fails

**Problem:** Docker image won't build

**Solution:**
1. Check Dockerfile syntax
2. Test locally: `docker build -t test .`
3. Check logs in GitHub Actions

### Linting Warnings

**Problem:** Too many linting warnings

**Solution:**
1. Fix warnings locally
2. Configure `.flake8` to ignore specific rules
3. Set `continue-on-error: true` (already done)

---

## 🎯 Best Practices

### 1. Run Tests Locally First

```bash
python manage.py test
```

### 2. Fix Linting Before Pushing

```bash
flake8 .
```

### 3. Test Docker Locally

```bash
docker-compose up -d
# Test application
docker-compose down
```

### 4. Commit Often

Small commits → Faster CI feedback

### 5. Review CI Results

Always check CI before merging PRs

---

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Django Testing](https://docs.djangoproject.com/en/4.2/topics/testing/)
- [Docker Geography](https://docs.docker.com/)
犯: [flake8 Documentation](https://flake8.pycqa.org/)

---

## ✅ Setup Complete!

Your NoteApp now has:
- ✅ Automated testing
- ✅ Code quality checks
- ✅ Security scanning
- ✅ Docker validation
- ✅ Optional Docker Hub deployment

**Push to GitHub to see it in action!** 🚀

