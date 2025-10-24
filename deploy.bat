@echo off
REM 🚀 Vercel Deployment Script for Note-Taking App (Windows)
REM This script automates the deployment process

echo 🚀 Starting Vercel deployment process...
echo ========================================

REM Check if Vercel CLI is installed
vercel --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Vercel CLI not found. Installing...
    npm install -g vercel
)

REM Check if user is logged in
vercel whoami >nul 2>&1
if errorlevel 1 (
    echo 🔐 Please login to Vercel first:
    vercel login
)

echo 📦 Deploying to Vercel...
vercel

echo 🔧 Setting up environment variables...
echo Please set the following environment variables in Vercel dashboard:
echo.
echo 1. DATABASE_URL - Your Supabase PostgreSQL connection string
echo 2. OPENAI_API_KEY - Your OpenAI API key
echo 3. GITHUB_TOKEN - Your GitHub personal access token
echo 4. SECRET_KEY - A random secret key for Flask
echo 5. FLASK_ENV - Set to 'production'
echo.

pause

echo 🔄 Redeploying with environment variables...
vercel --prod

echo ✅ Deployment complete!
echo Your app should be available at the URL provided above.
echo.
echo Next steps:
echo 1. Set up your Supabase database
echo 2. Run the database migration script
echo 3. Test your deployed application
echo.
echo For detailed instructions, see DEPLOYMENT.md

pause
