# Deploying Briefroom to Render

This guide will walk you through deploying your Briefroom application to Render, a modern cloud platform that makes deployment simple and affordable.

## Prerequisites

Before starting, make sure you have:
- Your Briefroom code in a Git repository (GitHub, GitLab, or Bitbucket)
- An OpenAI API key
- A Render account (free tier available)

## Step 1: Prepare Your Repository

1. **Ensure your code is in a Git repository**
   - If not already done, push your Briefroom code to GitHub, GitLab, or Bitbucket
   - Make sure all files are committed and pushed

2. **Required files are already created**
   Your repository now includes:
   - `render.yaml` - Render configuration file
   - `runtime.txt` - Python version specification
   - `pyproject.toml` - Dependencies configuration

## Step 2: Create a Render Account

1. **Sign up for Render**
   - Go to [render.com](https://render.com)
   - Click "Get Started" and create a free account
   - You can sign up with GitHub, GitLab, or email

2. **Connect your Git provider**
   - Render will ask to connect to your Git provider
   - Grant the necessary permissions to access your repositories

## Step 3: Create a New Web Service

1. **Create a new service**
   - From your Render dashboard, click "New +"
   - Select "Web Service"

2. **Connect your repository**
   - Find and select your Briefroom repository
   - Click "Connect"

3. **Configure your service**
   Fill in the following settings:

   **Basic Settings:**
   - **Name**: `briefroom` (or your preferred name)
   - **Environment**: `Python 3`
   - **Region**: Choose the region closest to your users
   - **Branch**: `main` (or your default branch)

   **Build & Deploy:**
   - **Build Command**: `pip install -e .`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 1 main:app`

   **Instance Type:**
   - **Free Tier**: Good for testing (spins down after 15 minutes of inactivity)
   - **Starter ($7/month)**: Recommended for production (always on)

## Step 4: Set Environment Variables

1. **Add environment variables**
   In the "Environment" section, add:

   ```
   OPENAI_API_KEY = your-openai-api-key-here
   SESSION_SECRET = your-secure-random-string-here
   PYTHON_VERSION = 3.11.0
   ```

   **Important Notes:**
   - Replace `your-openai-api-key-here` with your actual OpenAI API key
   - For `SESSION_SECRET`, generate a secure random string (you can use an online generator)
   - Don't use quotes around the values

2. **Database configuration (optional)**
   For production, you might want to use PostgreSQL:
   ```
   DATABASE_URL = postgresql://username:password@hostname:port/database
   ```
   (Render can provision a PostgreSQL database for you)

## Step 5: Deploy

1. **Click "Create Web Service"**
   - Render will start building and deploying your application
   - This process typically takes 2-5 minutes

2. **Monitor the deployment**
   - Watch the build logs for any errors
   - Common issues include missing dependencies or environment variables

3. **Access your application**
   - Once deployed, Render will provide a URL like `https://briefroom.onrender.com`
   - Your application will be live and accessible worldwide

## Step 6: Set Up a Database (Optional)

If you want to use PostgreSQL instead of SQLite:

1. **Create a PostgreSQL database**
   - From your Render dashboard, click "New +"
   - Select "PostgreSQL"
   - Choose a name and region
   - Select the free tier for testing

2. **Get the database URL**
   - Once created, copy the "External Database URL"
   - Add it as an environment variable: `DATABASE_URL`

3. **Redeploy your service**
   - Your web service will automatically restart with the new database

## Step 7: Configure Custom Domain (Optional)

1. **Add a custom domain**
   - In your web service settings, go to "Settings"
   - Scroll to "Custom Domains"
   - Add your domain (e.g., `briefroom.yourdomain.com`)

2. **Update DNS records**
   - Add a CNAME record pointing to your Render URL
   - Render will automatically provision SSL certificates

## Troubleshooting Common Issues

### Build Failures

**Issue**: Build fails with dependency errors
**Solution**: 
- Check that your `pyproject.toml` includes all required dependencies
- Verify Python version compatibility

**Issue**: "Module not found" errors
**Solution**: 
- Ensure all your Python files are in the repository
- Check import statements are correct

### Runtime Errors

**Issue**: "OpenAI API key not set" error
**Solution**: 
- Verify `OPENAI_API_KEY` is set in environment variables
- Check the key is valid and has sufficient credits

**Issue**: Application won't start
**Solution**: 
- Check the start command: `gunicorn --bind 0.0.0.0:$PORT main:app`
- Verify `main.py` exists and imports your Flask app correctly

### Performance Issues

**Issue**: App is slow or times out
**Solution**: 
- Upgrade from Free tier to Starter for better performance
- Optimize your database queries
- Consider adding Redis for caching

## Monitoring and Maintenance

1. **Monitor your application**
   - Use Render's built-in metrics and logs
   - Set up alerts for downtime or errors

2. **Regular updates**
   - Push updates to your Git repository
   - Render will automatically redeploy

3. **Backup your data**
   - If using PostgreSQL, set up regular backups
   - Export important analysis results periodically

## Cost Optimization

**Free Tier Limitations:**
- Application spins down after 15 minutes of inactivity
- 750 hours/month of usage
- Good for development and testing

**Paid Tier Benefits:**
- Always-on service (no spin-down)
- Better performance
- Custom domains
- More resources

## Security Best Practices

1. **Environment Variables**
   - Never commit API keys to your repository
   - Use Render's environment variable system
   - Rotate keys regularly

2. **HTTPS**
   - Render provides free SSL certificates
   - Always use HTTPS URLs

3. **Database Security**
   - Use strong passwords for database connections
   - Limit database access to necessary IPs only

## Support and Resources

- **Render Documentation**: [docs.render.com](https://docs.render.com)
- **Render Community**: [community.render.com](https://community.render.com)
- **Status Page**: [status.render.com](https://status.render.com)

## Example Environment Variables for Production

```bash
# Required
OPENAI_API_KEY=sk-your-actual-openai-key-here
SESSION_SECRET=your-very-secure-random-string-here

# Optional
DATABASE_URL=postgresql://user:pass@host:5432/briefroom_prod
PYTHON_VERSION=3.11.0

# Flask settings
FLASK_ENV=production
```

---

**Your Briefroom application is now live and ready to transform conversations into structured briefs!**

## Quick Deployment Checklist

- [ ] Code pushed to Git repository
- [ ] Render account created
- [ ] Web service configured
- [ ] Environment variables set
- [ ] OpenAI API key added
- [ ] Application deployed successfully
- [ ] Custom domain configured (optional)
- [ ] Database set up (if needed)
- [ ] SSL certificate active
- [ ] Application tested and working

Need help? Check the troubleshooting section above or contact Render support.