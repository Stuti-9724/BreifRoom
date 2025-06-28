# Render Deployment Troubleshooting Guide

## Common Deployment Issues and Solutions

### Issue 1: Build Command Errors

**Error**: `ERROR: Could not find a version that satisfies the requirement...`

**Solution**: Use the correct build command
```bash
# Correct build command for Render
pip install -e .
```

**In Render Dashboard**:
- Build Command: `pip install -e .`
- Start Command: `gunicorn --bind 0.0.0.0:$PORT --workers 1 main:app`

### Issue 2: Python Version Problems

**Error**: `python: command not found` or version conflicts

**Solution**: Ensure these files exist in your repository:
- `runtime.txt` containing: `python-3.11.0`
- `render.yaml` with correct Python configuration

### Issue 3: Environment Variables Not Set

**Error**: `OpenAI API key not set` or similar environment errors

**Solution**: In Render dashboard, go to Environment section and add:
```
OPENAI_API_KEY=sk-your-actual-key-here
SESSION_SECRET=your-random-secret-string
FLASK_ENV=production
```

### Issue 4: Import Errors

**Error**: `ModuleNotFoundError: No module named 'app'`

**Solution**: Ensure your start command points to the correct file:
```bash
gunicorn --bind 0.0.0.0:$PORT --workers 1 main:app
```

### Issue 5: Database Connection Issues

**Error**: Database connection failures in production

**Solution**: 
1. For SQLite (default): No additional setup needed
2. For PostgreSQL: Add `DATABASE_URL` environment variable

## Step-by-Step Deployment Process

### Method 1: Using Render Dashboard (Recommended)

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Create Render Web Service**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your Briefroom repository

3. **Configure Service Settings**
   ```
   Name: briefroom
   Environment: Python 3
   Build Command: pip install -e .
   Start Command: gunicorn --bind 0.0.0.0:$PORT --workers 1 main:app
   ```

4. **Set Environment Variables**
   ```
   OPENAI_API_KEY = sk-your-openai-key
   SESSION_SECRET = your-secure-random-string
   FLASK_ENV = production
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete (5-10 minutes)

### Method 2: Using render.yaml (Alternative)

Your repository already includes `render.yaml`. Just:
1. Push to GitHub
2. Import repository to Render
3. Set environment variables
4. Deploy

## Debugging Build Logs

### Reading Render Logs

1. **Build Logs**: Show dependency installation
2. **Deploy Logs**: Show application startup
3. **Service Logs**: Show runtime errors

### Common Log Messages

**Success**:
```
[INFO] Starting gunicorn
[INFO] Listening at: http://0.0.0.0:10000
[INFO] Booting worker with pid: xxx
```

**Failure**:
```
[ERROR] Worker failed to boot
ModuleNotFoundError: No module named 'openai'
```

## Environment Variable Setup

### Required Variables
```bash
OPENAI_API_KEY=sk-proj-xxx  # Your OpenAI API key
SESSION_SECRET=random-secure-string  # Generate a secure random string
```

### Optional Variables
```bash
DATABASE_URL=postgresql://...  # For PostgreSQL (optional)
FLASK_ENV=production  # Production environment
```

### Generating SESSION_SECRET
Use any of these methods:
```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Online generator
# Visit: https://randomkeygen.com/
```

## File Structure Checklist

Ensure your repository has these files:
```
├── app.py
├── main.py
├── models.py
├── routes.py
├── ai_service.py
├── pdf_service.py
├── pyproject.toml  ✓
├── render.yaml     ✓
├── runtime.txt     ✓
├── static/
├── templates/
└── uploads/
```

## Testing Deployment Locally

Before deploying to Render, test locally:

```bash
# Install dependencies
pip install -e .

# Set environment variables
export OPENAI_API_KEY="sk-your-key"
export SESSION_SECRET="your-secret"

# Run with gunicorn (same as Render)
gunicorn --bind 0.0.0.0:5000 --workers 1 main:app
```

## Quick Fixes

### Fix 1: Dependency Issues
If dependencies fail to install:
```bash
# Ensure pyproject.toml has all dependencies
# Check versions are compatible
```

### Fix 2: App Won't Start
```bash
# Check main.py imports app correctly
# Verify gunicorn command syntax
```

### Fix 3: Runtime Errors
```bash
# Check environment variables are set
# Verify OpenAI API key is valid
# Check file permissions
```

## Alternative Deployment Platforms

If Render continues to have issues, consider:

1. **Railway**: Similar to Render, Python-friendly
2. **Vercel**: Good for Flask apps
3. **Heroku**: Traditional PaaS platform
4. **DigitalOcean App Platform**: Simple deployment

## Getting Help

1. **Render Support**: help@render.com
2. **Check Status**: status.render.com
3. **Community**: community.render.com
4. **Documentation**: docs.render.com

## Emergency Deployment Script

If all else fails, here's a minimal deployment script:

```python
# deploy.py
import os
import subprocess

def deploy_to_render():
    print("Preparing for Render deployment...")
    
    # Check required files
    required_files = ['main.py', 'app.py', 'pyproject.toml']
    for file in required_files:
        if not os.path.exists(file):
            print(f"ERROR: Missing {file}")
            return False
    
    # Check environment variables
    if not os.getenv('OPENAI_API_KEY'):
        print("WARNING: OPENAI_API_KEY not set")
    
    print("✓ All checks passed. Ready for deployment!")
    return True

if __name__ == "__main__":
    deploy_to_render()
```

Run with: `python deploy.py`

---

**Need immediate help?** Contact me with:
1. Error logs from Render
2. Your repository URL
3. Environment variables you've set (without actual values)

The most common issue is incorrect build commands or missing environment variables. Double-check these first!