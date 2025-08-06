# Deployment Guide - Guinness App

## Current Deployment Setup

### Platform: Railway
- **Project**: xtrillion-demo
- **Environments**: 
  - Production: https://x-trillion.ai (or similar)
  - Development: https://dev.x-trillion.ai
- **Service Name**: Likely "zooming-appreciation" or "amusing-insight"

### Repository Structure
```
xtrillion_guinness_app/
├── guinness_app.py          # Main entry point
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container configuration
├── railway.json/toml       # Railway configuration
└── .streamlit/
    └── config.toml         # Streamlit configuration
```

### Deployment Process

#### Automatic (via GitHub)
1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Update: description of changes"
   git push origin main  # or development branch
   ```

2. **Railway Auto-Deploy**:
   - Railway detects push to connected branch
   - Builds Docker container
   - Deploys to specified environment
   - Updates live URL

#### Manual (via Railway CLI)
```bash
# Link to project (one-time)
railway link

# Deploy
railway up

# Check logs
railway logs
```

### Environment Variables

Set in Railway dashboard:
```
RAILWAY_ENVIRONMENT=production  # or development
STREAMLIT_SERVER_PORT=$PORT
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Build Configuration

**Dockerfile**:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "guinness_app.py", "--server.port=$PORT", "--server.address=0.0.0.0"]
```

**railway.json**:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "startCommand": "streamlit run guinness_app.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Monitoring

1. **Railway Dashboard**:
   - View deployment status
   - Check build logs
   - Monitor resource usage
   - View environment variables

2. **Application Logs**:
   ```bash
   railway logs --tail 100
   ```

3. **Debug Page**:
   - Visit `/debug` on deployed app
   - Shows deployment info, file status, etc.

### Rollback Process

If deployment fails:
1. Go to Railway dashboard
2. Click on service
3. Go to "Deployments" tab
4. Find previous working deployment
5. Click "Rollback" or "Redeploy"

### Common Issues

1. **Port Binding**:
   - Ensure using `$PORT` environment variable
   - Not hardcoded 8501

2. **Dependencies**:
   - Keep requirements.txt updated
   - Test locally first

3. **Memory**:
   - Railway free tier has limits
   - Monitor usage in dashboard

### Local Testing

Before deploying:
```bash
# Test locally
streamlit run guinness_app.py

# Test with production settings
PORT=8501 streamlit run guinness_app.py --server.address=0.0.0.0

# Build Docker locally
docker build -t guinness-app .
docker run -p 8501:8501 guinness-app
```