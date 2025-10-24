# 🚀 Vercel Deployment Guide

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Supabase Account**: Sign up at [supabase.com](https://supabase.com)
3. **GitHub Repository**: Push your code to GitHub
4. **API Keys**: OpenAI and GitHub tokens

## Step 1: Set Up Supabase Database

### 1.1 Create Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Click "New Project"
3. Choose your organization
4. Enter project details:
   - **Name**: `note-taking-app`
   - **Database Password**: Generate a strong password
   - **Region**: Choose closest to your users

### 1.2 Get Database Connection String
1. Go to **Settings** → **Database**
2. Copy the **Connection string** (URI)
3. Replace `[YOUR-PASSWORD]` with your database password
4. Example: `postgresql://postgres:yourpassword@db.abcdefgh.supabase.co:5432/postgres`

## Step 2: Deploy to Vercel

### 2.1 Using Vercel CLI (Recommended)

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy from project directory
vercel

# Follow the prompts:
# - Set up and deploy? Y
# - Which scope? [Your account]
# - Link to existing project? N
# - What's your project's name? note-taking-app
# - In which directory is your code located? ./
```

### 2.2 Set Environment Variables

   ```bash
# Set database URL
vercel env add DATABASE_URL

# Set OpenAI API key
vercel env add OPENAI_API_KEY

# Set GitHub token
vercel env add GITHUB_TOKEN

# Set secret key
vercel env add SECRET_KEY

# Set Flask environment
vercel env add FLASK_ENV production
```

### 2.3 Redeploy with Environment Variables

```bash
# Redeploy to apply environment variables
vercel --prod
```

## Step 3: Initialize Database

### 3.1 Run Database Migration

```bash
# Set DATABASE_URL environment variable locally
export DATABASE_URL="postgresql://postgres:yourpassword@db.abcdefgh.supabase.co:5432/postgres"

# Run migration script
cd backend
python migrate_to_postgres.py

# Initialize database
python init_db.py
```

## Step 4: Test Deployment

### 4.1 Health Check
Visit: `https://your-app.vercel.app/api/health`

Expected response:
```json
{
  "status": "healthy"
}
```

### 4.2 Test API Endpoints
- **GET** `/api/notes` - List all notes
- **POST** `/api/notes` - Create new note
- **GET** `/api/notes/search?q=query` - Search notes

## Step 5: Frontend Deployment

### 5.1 Build Frontend
```bash
cd frontend
npm run build
```

### 5.2 Deploy Frontend
The frontend will be automatically deployed with the Vercel deployment.

## Troubleshooting

### Common Issues

#### 1. Database Connection Error
- **Check**: DATABASE_URL is correctly set
- **Verify**: Supabase project is active
- **Test**: Connection string in database client

#### 2. CORS Error
- **Check**: CORS origins in `backend/app.py`
- **Verify**: Frontend URL matches CORS configuration
- **Update**: Add your Vercel domain to CORS origins

#### 3. Environment Variables Not Loading
- **Check**: Variables are set in Vercel dashboard
- **Verify**: Variable names match exactly
- **Redeploy**: Run `vercel --prod` after setting variables

#### 4. Build Failures
- **Check**: All dependencies in `requirements.txt`
- **Verify**: Python version compatibility
- **Review**: Build logs in Vercel dashboard

### Debug Commands

```bash
# Check Vercel deployment status
vercel ls

# View deployment logs
vercel logs [deployment-url]

# Check environment variables
vercel env ls

# Test locally with production environment
vercel dev
```

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:port/db` |
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |
| `GITHUB_TOKEN` | GitHub personal access token | `ghp_...` |
| `SECRET_KEY` | Flask secret key | `your-secret-key` |
| `FLASK_ENV` | Flask environment | `production` |

## Production Checklist

- [ ] Supabase database created and configured
- [ ] Environment variables set in Vercel
- [ ] Database migration completed
- [ ] Health check endpoint working
- [ ] API endpoints responding correctly
- [ ] Frontend accessible and functional
- [ ] CORS configuration working
- [ ] Error handling in place
- [ ] Monitoring set up (optional)

## Security Considerations

1. **Environment Variables**: Never commit sensitive data to repository
2. **Database Access**: Use connection pooling and proper authentication
3. **API Keys**: Rotate keys regularly
4. **CORS**: Restrict origins to known domains only
5. **HTTPS**: Vercel provides automatic HTTPS

## Performance Optimization

1. **Database Indexing**: Add indexes for frequently queried fields
2. **Connection Pooling**: Configure database connection pooling
3. **Caching**: Implement Redis caching for frequently accessed data
4. **CDN**: Vercel provides automatic CDN for static assets

## Monitoring and Maintenance

1. **Vercel Analytics**: Monitor performance and usage
2. **Database Monitoring**: Use Supabase dashboard
3. **Error Tracking**: Consider adding Sentry or similar
4. **Logs**: Monitor Vercel function logs

---

**Need Help?** Check the [Vercel Documentation](https://vercel.com/docs) or [Supabase Documentation](https://supabase.com/docs)