# Deployment Checklist

## Pre-Deployment Verification

### ✅ Local Testing
- [x] App runs locally with `streamlit run guinness_app.py`
- [x] All imports work correctly
- [x] Navigation structure is valid

### ✅ Git Configuration
- [x] Repository: https://github.com/urbancanary/xtrillion-railway-demo
- [x] Branch: develop
- [x] All changes committed and pushed

### ✅ File Updates
- [x] Entry point renamed: `xtrillion_guinness_nav.py` → `guinness_app.py`
- [x] Dockerfile updated to use `guinness_app.py`
- [x] Unused files archived
- [x] Documentation created

## Railway Configuration

### Environment Variables to Check
In Railway dashboard, ensure these are set:
```
RAILWAY_ENVIRONMENT=development  # or production
PORT=$PORT                      # Railway provides this
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### Deployment Settings
- **Source**: GitHub repository
- **Branch**: develop (for dev.x-trillion.ai)
- **Build**: Docker (using Dockerfile)
- **Start Command**: Defined in Dockerfile

## Post-Deployment Verification

### 1. Check Railway Dashboard
- [ ] Build logs show successful build
- [ ] Deploy logs show app started
- [ ] No error messages

### 2. Test Live Site
- [ ] Visit dev.x-trillion.ai
- [ ] Navigation works
- [ ] All pages load
- [ ] Data displays correctly

### 3. Monitor Logs
```bash
railway logs --tail 100
```

## If Deployment Fails

### Common Issues:

1. **Module Import Error**
   - Check requirements.txt has all dependencies
   - Verify file paths are correct

2. **Port Binding Error**
   - Ensure using $PORT environment variable
   - Not hardcoded to 8501

3. **Entry Point Not Found**
   - Verify Dockerfile uses `guinness_app.py`
   - Check file exists and is committed

4. **Build Timeout**
   - Reduce Docker image size
   - Check for unnecessary dependencies

### Quick Fixes:

1. **Rollback**:
   - Go to Railway dashboard
   - Find last working deployment
   - Click "Redeploy"

2. **Manual Trigger**:
   - In Railway dashboard
   - Click "Deploy" button
   - Select develop branch

## Success Indicators

- ✅ Railway shows "Deployed" status
- ✅ Site loads at dev.x-trillion.ai
- ✅ No errors in logs
- ✅ All functionality works as in local testing