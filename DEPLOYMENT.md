# Deployment Guide

## Environment Variables

### Backend Environment Variables
```bash
# Database URL (for production)
DATABASE_URL=postgresql://user:password@host:port/database

# Flask settings
FLASK_ENV=production
SECRET_KEY=your-secret-key-here

# CORS settings
CORS_ORIGINS=https://your-frontend-domain.com
```

### Frontend Environment Variables
```bash
# API URL (switch from local to production)
REACT_APP_API_URL=https://your-backend-domain.com/api

# Optional: Analytics, error tracking, etc.
REACT_APP_ANALYTICS_ID=your-analytics-id
```

## Frontend Deployment (Vercel)

1. **Prepare for production**:
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy to Vercel**:
   - Connect GitHub repository to Vercel
   - Set build command: `npm run build`
   - Set output directory: `build`
   - Add environment variable: `REACT_APP_API_URL=https://your-backend-url.com/api`

3. **Custom domain** (optional):
   - Add custom domain in Vercel dashboard
   - Update CORS settings in backend

## Backend Deployment (Render)

1. **Prepare for production**:
   ```bash
   cd backend
   # Create requirements.txt (already done)
   # Create Procfile for Render
   ```

2. **Create Procfile**:
   ```
   web: gunicorn app:app
   ```

3. **Update requirements.txt** for production:
   ```
   Flask==2.3.3
   Flask-CORS==4.0.0
   SQLAlchemy==2.0.21
   python-dateutil==2.8.2
   gunicorn==21.2.0
   psycopg2-binary==2.9.7
   ```

4. **Deploy to Render**:
   - Connect GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `gunicorn app:app`
   - Add environment variables
   - Enable auto-deploy from main branch

## Database Migration for Production

### Option 1: PostgreSQL (Recommended)
```python
# Update models.py for production
import os
from sqlalchemy import create_engine

# Use environment variable for database URL
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///notes.db')
engine = create_engine(DATABASE_URL, echo=False)
```

### Option 2: Keep SQLite (Simple)
- SQLite works for small to medium applications
- File-based, no external database needed
- Limited concurrent access

## Environment Configuration

### Development
- Backend: `http://localhost:5000`
- Frontend: `http://localhost:3000`
- Database: SQLite file

### Production
- Backend: `https://your-app.onrender.com`
- Frontend: `https://your-app.vercel.app`
- Database: PostgreSQL or SQLite

## Security Considerations

1. **CORS Configuration**:
   ```python
   # In app.py
   CORS(app, origins=[
       "http://localhost:3000",  # Development
       "https://your-frontend-domain.com"  # Production
   ])
   ```

2. **Environment Variables**:
   - Never commit `.env` files
   - Use secure secret keys
   - Rotate keys regularly

3. **Database Security**:
   - Use connection pooling
   - Enable SSL for production database
   - Regular backups

## Monitoring and Logging

### Backend Logging
```python
import logging
from flask import Flask

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/api/health')
def health_check():
    app.logger.info('Health check requested')
    return jsonify({'status': 'healthy'})
```

### Frontend Error Tracking
```typescript
// Add to App.tsx
window.addEventListener('error', (event) => {
  console.error('Global error:', event.error);
  // Send to error tracking service
});
```

## Performance Optimization

### Backend
- Add database indexes for search
- Implement pagination for large datasets
- Add caching for frequently accessed data

### Frontend
- Code splitting for large components
- Lazy loading for images
- Service worker for offline support

## Backup Strategy

### Database Backups
```bash
# SQLite backup
cp notes.db backup/notes-$(date +%Y%m%d).db

# PostgreSQL backup
pg_dump $DATABASE_URL > backup/notes-$(date +%Y%m%d).sql
```

### Automated Backups
- Set up cron job for daily backups
- Store backups in cloud storage
- Test restore procedures regularly

## Rollback Plan

1. **Frontend Rollback**:
   - Vercel: Revert to previous deployment
   - Keep previous build artifacts

2. **Backend Rollback**:
   - Render: Revert to previous deployment
   - Database: Restore from backup if needed

3. **Database Rollback**:
   - Restore from backup
   - Run migration rollback scripts

## Cost Estimation

### Vercel (Frontend)
- Free tier: 100GB bandwidth/month
- Pro: $20/month for unlimited bandwidth

### Render (Backend)
- Free tier: 750 hours/month
- Starter: $7/month for always-on service

### Database
- PostgreSQL on Render: $7/month
- Or use free SQLite (file-based)

## Final Checklist

- [ ] Environment variables configured
- [ ] CORS settings updated
- [ ] Database migrated (if needed)
- [ ] SSL certificates working
- [ ] Error tracking enabled
- [ ] Backup strategy implemented
- [ ] Performance monitoring set up
- [ ] Documentation updated
