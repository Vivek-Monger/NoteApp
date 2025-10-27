# Docker Hub Integration - GitHub Actions

## 🐳 Overview

This project is configured to automatically build and push Docker images to Docker Hub when you push to the `main` branch.

---

## ✅ Setup Complete

The workflow file (`.github/workflows/ci.yml`) has been updated to:
- ✅ Login to Docker Hub using GitHub Secrets
- ✅ Build the Docker image
- ✅ Push the image to Docker Hub
- ✅ Only push on main branch
- ✅ Use proper authentication tokens

---

## 🔑 Required GitHub Secrets

You need to add these secrets to your GitHub repository:

### Step 1: Get a Docker Hub Access Token

1. Go to [Docker Hub](https://hub.docker.com/)
2. Click on your profile → **Account Settings**
3. Go to **Security** → **New Access Token**
4. Name it: `github-actions` (or any name you prefer)
5. Set permissions: **Read, Write, Delete**
6. Click **Generate** and **copy the token**

### Step 2: Add Secrets to GitHub

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these two secrets:

| Secret Name | Value |
|-------------|-------|
| `DOCKERHUB_USERNAME` | Your Docker Hub username |
| `DOCKERHUB_TOKEN` | The access token you just copied |

---

## 🔧 How It Works

### Workflow Triggers

The Docker image is built and pushed **only when:**
- ✅ You push to the `main` branch
- ✅ Docker Hub secrets are configured
- ✅ Pull requests do NOT trigger push (only build and test)

### Authentication

```yaml
- name: Login to Docker Hub
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}  # ← Access token, NOT password
```

**Important:** Use an **access token**, not your Docker Hub password.

### Image Tagging

```yaml
tags: ${{ secrets.DOCKERHUB_USERNAME }}/noteapp:latest
```

Images are tagged as:
- `your-username/noteapp:latest`

---

## 📊 Workflow Steps

### 1. Test & Lint Job
- Runs on Python 3.10 and 3.11
- Tests code quality
- Runs Django tests

### 2. Docker Build & Test Job
- Builds Docker image
- Tests container startup
- **Pushes to Docker Hub** (only on main branch)

### 3. Security Scan Job
- Checks for vulnerabilities
- Runs security analysis

---

## 🚀 Usage

### Automatic Push

1. Make changes to your code
2. Commit and push to main branch:
   ```bash
   git add .
   git commit -m "Update NoteApp"
   git push origin main
   ```

3. CI automatically:
   - Runs tests
   - Builds Docker image
   - Pushes to Docker Hub
   - Tags as `your-username/noteapp:latest`

### Manual Push to Docker Hub

If you want to push manually:

```bash
# Build the image
docker build -t your-username/noteapp:latest .

# Login to Docker Hub
docker login

# Push the image
docker push your-username/noteapp:latest
```

---

## 🔍 Verifying the Push

### Check GitHub Actions

1. Go to your GitHub repository
2. Click on the **Actions** tab
3. Click on the latest workflow run
4. Look for the "Build and push Docker image" step
5. You should see:
   ```
   Pushed docker://your-username/noteapp:latest
   ```

### Check Docker Hub

1. Go to [Docker Hub](https://hub.docker.com/)
2. Search for your repository
3. You should see `your-username/noteapp`
4. The latest image should be marked as "latest"

---

## ⚠️ Common Issues

### Workflow Validation Error

**Problem:** "Unrecognized named-value: 'secrets'" error

**Solution:** Fixed! The workflow now properly handles GitHub Secrets.

### "401 Unauthorized" Error

**Problem:** Access denied when pushing to Docker Hub

**Solutions:**
1. Check that `DOCKERHUB_USERNAME` secret is correct
2. Check that `DOCKERHUB_TOKEN` secret is correct (access token, not password)
3. Make sure the token has **Write** permissions
4. Regenerate the token if needed
5. The workflow uses `continue-on-error: true` so it won't fail if secrets aren't configured

### "Repository not found" Error

**Problem:** Docker Hub can't find the repository

**Solutions:**
1. Make sure the repository name matches in the workflow
2. Check that the username in the secret is correct
3. The repository will be created automatically on first push

### Push Not Happening

**Problem:** Image isn't being pushed

**Solutions:**
1. Check that you're pushing to the `main` branch
2. Verify that the secrets are set up correctly
3. Check the workflow conditions in the `if` statements
4. Look at the workflow logs to see what's being skipped

---

## 📝 Workflow Configuration

Current settings in `.github/workflows/ci.yml`:

```yaml
# Only push on main branch pushes
if: github.event_name == 'push' && github.ref == 'refs/heads/main'

# Use GitHub Secrets
username: ${{ secrets.DOCKERHUB_USERNAME }}
password: ${{ secrets.DOCKERHUB_TOKEN }}

# Continue even if secrets are missing
continue-on-error: true

# Single tag as latest
tags: ${{ secrets.DOCKERHUB_USERNAME }}/noteapp:latest
```

---

## ✅ Verification Checklist

- [ ] Docker Hub account created
- [ ] Access token generated with Read/Write permissions
- [ ] GitHub Secrets added (DOCKERHUB_USERNAME and DOCKERHUB_TOKEN)
- [ ] Pushed to main branch
- [ ] GitHub Actions workflow completed successfully
- [ ] Image visible on Docker Hub

---

## 🎉 Summary

Your NoteApp is now configured to:
- ✅ Automatically build and push Docker images
- ✅ Push only on main branch
- ✅ Use secure token authentication
- ✅ Tag images as `your-username/noteapp:latest`

**Ready to push!** 🚀

