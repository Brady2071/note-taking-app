# Vercel Deployment Guide for Lab 2

## Prerequisites
- GitHub repository with Lab 2 code
- Supabase account (for database)
- GitHub account (for GitHub Models API)

## Step 1: Database Setup (Supabase)

### Create Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Note down:
   - Project URL
   - Database password
   - API keys

### Database Configuration
```sql
-- Run this in Supabase SQL editor
CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    tags TEXT,
    event_date DATE,
    event_time TIME,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create index for search
CREATE INDEX idx_notes_title_content ON notes USING gin(to_tsvector('english', title || ' ' || content));
```

## Step 2: Backend Deployment (Railway)

### Option A: Railway (Recommended)
1. Go to [railway.app](https://railway.app)
2. Connect GitHub repository
3. Select `backend` folder as root directory
4. Add environment variables:
   ```
   GITHUB_TOKEN=your_github_token
   DATABASE_URL=postgresql://postgres:password@host:port/postgres
   FLASK_ENV=production
   SECRET_KEY=your_secret_key
   ```
5. Deploy and note the URL (e.g., `https://your-app.railway.app`)

### Option B: Render
1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn app:app`
6. Add environment variables (same as above)

## Step 3: Frontend Deployment (Vercel)

### Deploy to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Import GitHub repository
3. Set build settings:
   - Framework Preset: Create React App
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `build`

### Environment Variables in Vercel
Add these in Vercel Dashboard → Project → Settings → Environment Variables:
```
REACT_APP_API_URL=https://your-backend-url.railway.app/api
```

## Step 4: GitHub Models API Setup

### Get GitHub Token
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Create new token with `read:packages` scope
3. Copy token and add to backend environment variables

### Test API Access
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://models.github.ai/inference \
     -d '{"model": "openai/gpt-4.1-mini", "messages": [{"role": "user", "content": "Hello"}]}'
```

## Step 5: Database Migration

### Run Migration Script
```bash
# Set environment variables
export DATABASE_URL="postgresql://postgres:password@host:port/postgres"
export GITHUB_TOKEN="your_token"

# Run migration
cd backend
python migrate_to_postgres.py
```

## Step 6: Testing Deployment

### Backend Health Check
```bash
curl https://your-backend-url.railway.app/api/health
```

### Frontend Test
1. Open your Vercel URL
2. Test note creation
3. Test translation feature
4. Test note generation
5. Verify database persistence

## Step 7: Production Configuration

### Backend Optimizations
```python
# In app.py, add for production
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### Frontend Environment Variables
Create `.env.production`:
```
REACT_APP_API_URL=https://your-backend-url.railway.app/api
```

## Step 8: Monitoring and Logs

### Railway Logs
- View logs in Railway dashboard
- Monitor API usage and errors

### Vercel Analytics
- Enable Vercel Analytics in dashboard
- Monitor frontend performance

### Database Monitoring
- Use Supabase dashboard for query monitoring
- Set up alerts for high usage

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Update CORS origins in backend
   - Add Vercel domain to allowed origins

2. **Database Connection Issues**
   - Verify DATABASE_URL format
   - Check Supabase connection settings

3. **API Key Issues**
   - Verify GITHUB_TOKEN is set correctly
   - Check token permissions

4. **Build Failures**
   - Check Node.js version compatibility
   - Verify all dependencies are installed

### Debug Commands
```bash
# Check backend logs
railway logs

# Check frontend build
vercel logs

# Test database connection
psql $DATABASE_URL -c "SELECT COUNT(*) FROM notes;"
```

## Security Checklist

- [ ] GITHUB_TOKEN is secure and not logged
- [ ] DATABASE_URL uses SSL
- [ ] CORS is properly configured
- [ ] Environment variables are not exposed
- [ ] API endpoints have proper validation
- [ ] Rate limiting is implemented

## Performance Optimization

### Backend
- Enable database connection pooling
- Add Redis for caching (optional)
- Implement request rate limiting

### Frontend
- Enable Vercel Edge Functions
- Optimize bundle size
- Add service worker for offline support

## Cost Estimation

### Vercel (Frontend)
- Free tier: 100GB bandwidth/month
- Pro: $20/month for unlimited

### Railway (Backend)
- Free tier: 500 hours/month
- Pro: $5/month for always-on

### Supabase (Database)
- Free tier: 500MB database
- Pro: $25/month for 8GB

## Final Deployment Checklist

- [ ] Backend deployed and healthy
- [ ] Database migrated and accessible
- [ ] Frontend deployed and connected to backend
- [ ] All environment variables set
- [ ] Translation feature working
- [ ] Note generation working
- [ ] Search functionality working
- [ ] Error handling working
- [ ] Mobile responsive design working
- [ ] Performance acceptable

## Rollback Plan

1. **Frontend Rollback**: Revert to previous Vercel deployment
2. **Backend Rollback**: Revert to previous Railway deployment
3. **Database Rollback**: Restore from Supabase backup
4. **Code Rollback**: Revert to previous Git commit

## Support and Maintenance

### Regular Tasks
- Monitor API usage and costs
- Update dependencies monthly
- Backup database weekly
- Review error logs daily

### Scaling Considerations
- Add load balancing for high traffic
- Implement database read replicas
- Add CDN for static assets
- Consider microservices architecture
