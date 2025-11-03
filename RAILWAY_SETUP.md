# Railway Deployment Guide

## Step-by-Step Setup

### 1. Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub (recommended) or email
3. Verify your account

### 2. Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Authorize Railway to access your GitHub
4. Select your `ai-screenshot-organizer` repository
5. Click "Deploy Now"

### 3. Configure Service
1. Railway should auto-detect Python
2. If not, click on your service → Settings → **Root Directory**: Set to `backend`
3. Click "Generate Domain" to get your Railway URL (e.g., `your-app.up.railway.app`)

### 4. Set Environment Variables
Go to your service → **Variables** tab and add:

```
# AWS Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
AWS_S3_BUCKET=your-s3-bucket-name

# Database (if using PostgreSQL)
DATABASE_URL=your_postgresql_url

# OpenAI
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-3.5-turbo

# CORS - Add your frontend URL
ALLOWED_ORIGINS=https://your-frontend-url.com,https://your-frontend-url.vercel.app
```

### 5. Update Frontend API URL
Once Railway gives you the backend URL, update your frontend:

1. In `frontend/src/services/api.ts`, update:
```typescript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://your-app.up.railway.app';
```

2. If deploying frontend separately, set `REACT_APP_API_URL` environment variable there too.

### 6. Add Tesseract OCR (System Dependency)
Railway needs Tesseract OCR installed. Railway will use the Dockerfile automatically if present.

The Dockerfile we created includes Tesseract installation.

### 7. Deploy Frontend (Optional - Railway)
1. Create another service for frontend
2. Set Root Directory to `frontend`
3. Railway will auto-detect React
4. Add environment variable: `REACT_APP_API_URL=https://your-backend.up.railway.app`

## Verification

1. **Check Health Endpoint:**
   ```
   https://your-app.up.railway.app/health
   ```
   Should return: `{"status": "healthy", ...}`

2. **Check API Docs:**
   ```
   https://your-app.up.railway.app/docs
   ```

3. **Test Upload:**
   - Go to your frontend
   - Try uploading an image
   - Check Railway logs if it fails

## Troubleshooting

### Build Fails
- Check logs in Railway dashboard
- Ensure `requirements.txt` has all dependencies
- Verify Python version (Railway uses 3.12 by default)

### 500 Errors
- Check environment variables are set correctly
- Verify AWS credentials
- Check Railway logs for specific error messages

### CORS Errors
- Add your frontend URL to `ALLOWED_ORIGINS` environment variable
- Format: `https://domain1.com,https://domain2.com` (comma-separated, no spaces)

### Tesseract Not Found
- The Dockerfile includes Tesseract installation
- If issues persist, check Railway build logs

## Monitoring

Railway provides:
- Real-time logs
- Metrics dashboard
- Automatic HTTPS
- Custom domains (Pro plan)

## Costs

- **Free tier:** $5 credit/month
- **Pay-as-you-go:** After free tier
- **Typical FastAPI app:** ~$5-10/month

## Next Steps

1. ✅ Deploy backend on Railway
2. ✅ Get backend URL
3. ✅ Update frontend API URL
4. ✅ Deploy frontend (Railway or Vercel)
5. ✅ Test full application
6. ✅ Update CORS settings with production URLs

## Pro Tips

- Use Railway's built-in PostgreSQL for database (if you want managed DB)
- Set up custom domain for production
- Use Railway's monitoring for production apps
- Enable auto-deploy on git push (default)

