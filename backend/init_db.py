#!/usr/bin/env python3
"""
Database initialization script for PostgreSQL
Creates tables and initializes the database
"""

import os
from models import Base, engine

def init_database():
    """Initialize the PostgreSQL database with required tables"""
    
    # Check if DATABASE_URL is set
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL environment variable not set!")
        print("Please set DATABASE_URL to your PostgreSQL connection string")
        return False
    
    try:
        print("📋 Creating database tables...")
        Base.metadata.create_all(engine)
        print("✅ Database tables created successfully!")
        
        # Test database connection
        from models import SessionLocal
        db = SessionLocal()
        try:
            # Test query
            result = db.execute("SELECT 1").fetchone()
            print("✅ Database connection test successful!")
        except Exception as e:
            print(f"⚠️  Database connection test failed: {e}")
        finally:
            db.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Initializing PostgreSQL database...")
    print("=" * 40)
    
    success = init_database()
    
    if success:
        print("=" * 40)
        print("✅ Database initialization completed!")
    else:
        print("=" * 40)
        print("❌ Database initialization failed!")