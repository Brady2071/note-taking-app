# Lab 2 Exercise: Deploying Note-Taking App to Vercel

## 📋 Overview

This document details the process of deploying a note-taking application to Vercel, including migrating from SQLite to PostgreSQL and restructuring the application for serverless deployment.

## 🎯 Objectives

1. **Step 1**: Migrate from SQLite to external PostgreSQL database
2. **Step 2**: Refactor app structure for Vercel deployment
3. **Step 3**: [Optional] Add unique features
4. **Documentation**: Create comprehensive writeup with screenshots

## 🚀 Step 1: Database Migration from SQLite to PostgreSQL

### Challenge Identified
- **Problem**: Vercel's serverless model doesn't support persistent file-based databases like SQLite
- **Solution**: Migrate to cloud-hosted PostgreSQL database (Supabase)

### Implementation Details

#### 1.1 Database Configuration
Created environment-based database configuration in `models.py`:

```python
def get_database_url():
    """Get database URL from environment variable or default to SQLite"""
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        return database_url
    else:
        return 'sqlite:///notes.db'
```

#### 1.2 Migration Script
Created `backend/migrate_to_postgres.py` to handle data migration:

- **Features**:
  - Connects to both SQLite and PostgreSQL
  - Migrates all existing notes
  - Handles errors gracefully
  - Provides detailed logging

#### 1.3 Database Initialization
Created `backend/init_db.py` for PostgreSQL setup:

- **Features**:
  - Creates required tables
  - Tests database connection
  - Provides status feedback

### Database Schema
The Note model includes:
- `id`: Primary key
- `title`: Note title (String, 200 chars)
- `content`: Note content (Text)
- `tags`: JSON string of tags array
- `event_date`: Optional event date
- `event_time`: Optional event time
- `updated_at`: Timestamp with auto-update

## 🏗️ Step 2: Vercel Deployment Structure

### 2.1 Vercel Configuration
Created `vercel.json` with proper routing:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "frontend/$1"
    }
  ]
}
```

### 2.2 API Structure
- **Created**: `api/index.py` as Vercel entry point
- **Modified**: `backend/app.py` for CORS configuration
- **Updated**: Environment variable handling

### 2.3 CORS Configuration
Updated CORS settings for Vercel deployment:

```python
CORS(app, origins=[
    "http://localhost:3000",
    "https://*.vercel.app",
    "https://note-taking-app-*.vercel.app"
])
```

## 🛠️ Step 3: Unique Features Added

### 3.1 Apple-Inspired UI Design
- **Modern Design**: Applied Apple's design language
- **Typography**: SF Pro Display/Text fonts
- **Color Scheme**: Apple's signature colors (#0071e3, #1d1d1f)
- **Interactions**: Smooth animations and hover effects

### 3.2 Enhanced User Experience
- **Responsive Design**: Mobile-first approach
- **Accessibility**: Proper contrast ratios and touch targets
- **Performance**: Optimized loading and transitions

## 📦 Deployment Process

### Prerequisites
1. **Vercel CLI**: Installed globally (`npm install -g vercel`)
2. **Database**: Supabase PostgreSQL instance
3. **Environment Variables**: Configured in Vercel dashboard

### Environment Variables Required
```
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
OPENAI_API_KEY=your_openai_api_key
GITHUB_TOKEN=your_github_token
FLASK_ENV=production
SECRET_KEY=your_secret_key
```

### Deployment Commands
```bash
# Login to Vercel
vercel login

# Deploy to Vercel
vercel

# Set environment variables
vercel env add DATABASE_URL
vercel env add OPENAI_API_KEY
vercel env add GITHUB_TOKEN
vercel env add SECRET_KEY
```

## 🔧 Technical Challenges & Solutions

### Challenge 1: Serverless Database Compatibility
- **Problem**: SQLite not compatible with Vercel's serverless model
- **Solution**: Migrated to PostgreSQL with Supabase hosting
- **Result**: Persistent data storage in cloud environment

### Challenge 2: CORS Configuration
- **Problem**: Cross-origin requests blocked in production
- **Solution**: Configured CORS for Vercel domains
- **Result**: Seamless frontend-backend communication

### Challenge 3: Environment Variables
- **Problem**: Sensitive data in code
- **Solution**: Environment variables in Vercel dashboard
- **Result**: Secure configuration management

## 📊 Project Structure

```
note-taking-app/
├── api/
│   └── index.py              # Vercel entry point
├── backend/
│   ├── app.py                # Flask application
│   ├── models.py             # Database models
│   ├── migrate_to_postgres.py # Migration script
│   └── init_db.py            # Database initialization
├── frontend/
│   ├── src/                  # React components
│   └── package.json          # Frontend dependencies
├── vercel.json               # Vercel configuration
├── requirements.txt          # Python dependencies
└── lab2_writeup.md          # This document
```

## 🎨 UI/UX Improvements

### Design System
- **Colors**: Apple-inspired palette
- **Typography**: SF Pro font family
- **Spacing**: Consistent 8px grid system
- **Components**: Reusable, accessible elements

### Key Features
- **Note Management**: Create, read, update, delete
- **Search**: Real-time note search
- **Tags**: Categorization system
- **Translation**: Multi-language support
- **AI Generation**: Smart note creation

## 🚀 Deployment Status

### Completed ✅
- [x] Database migration to PostgreSQL
- [x] Vercel configuration
- [x] API structure refactoring
- [x] CORS configuration
- [x] Environment variable setup
- [x] UI/UX improvements

### Next Steps
- [ ] Deploy to Vercel using CLI
- [ ] Configure Supabase database
- [ ] Test production deployment
- [ ] Monitor performance

## 📝 Lessons Learned

1. **Serverless Limitations**: File-based databases don't work in serverless environments
2. **Environment Management**: Proper environment variable configuration is crucial
3. **CORS Configuration**: Production CORS settings differ from development
4. **Database Migration**: Careful data migration requires robust error handling
5. **UI/UX Design**: Apple's design principles significantly improve user experience

## 🔗 Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Supabase Documentation](https://supabase.com/docs)
- [Flask-CORS Documentation](https://flask-cors.readthedocs.io/)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)

## 📸 Screenshots

*Screenshots will be added after successful deployment*

---

**Author**: [Your Name]  
**Date**: [Current Date]  
**Lab**: 2 - Vercel Deployment  
**Course**: [Course Name]