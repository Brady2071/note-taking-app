#!/usr/bin/env python3
"""
Database migration script from SQLite to PostgreSQL
Run this script to migrate existing SQLite data to PostgreSQL
"""

import os
import json
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Note, Base
from datetime import datetime

def migrate_sqlite_to_postgres():
    """Migrate data from SQLite to PostgreSQL"""
    
    # Check if DATABASE_URL is set
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL environment variable not set!")
        print("Please set DATABASE_URL to your PostgreSQL connection string")
        return False
    
    # SQLite connection (local database)
    sqlite_url = 'sqlite:///notes.db'
    sqlite_engine = create_engine(sqlite_url)
    sqlite_session = sessionmaker(bind=sqlite_engine)()
    
    # PostgreSQL connection
    postgres_engine = create_engine(database_url)
    postgres_session = sessionmaker(bind=postgres_engine)()
    
    try:
        # Create tables in PostgreSQL
        print("📋 Creating tables in PostgreSQL...")
        Base.metadata.create_all(postgres_engine)
        
        # Check if SQLite database exists and has data
        try:
            sqlite_notes = sqlite_session.query(Note).all()
            print(f"📊 Found {len(sqlite_notes)} notes in SQLite database")
            
            if len(sqlite_notes) == 0:
                print("ℹ️  No data to migrate from SQLite")
                return True
            
            # Migrate each note
            migrated_count = 0
            for note in sqlite_notes:
                try:
                    # Create new note in PostgreSQL
                    new_note = Note(
                        title=note.title,
                        content=note.content,
                        tags=note.tags,
                        event_date=note.event_date,
                        event_time=note.event_time,
                        updated_at=note.updated_at
                    )
                    postgres_session.add(new_note)
                    migrated_count += 1
                    
                except Exception as e:
                    print(f"⚠️  Error migrating note {note.id}: {e}")
                    continue
            
            # Commit all changes
            postgres_session.commit()
            print(f"✅ Successfully migrated {migrated_count} notes to PostgreSQL")
            
        except Exception as e:
            print(f"⚠️  SQLite database not found or empty: {e}")
            print("ℹ️  Proceeding with empty PostgreSQL database")
        
        # Verify migration
        postgres_notes = postgres_session.query(Note).all()
        print(f"📊 PostgreSQL database now contains {len(postgres_notes)} notes")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        postgres_session.rollback()
        return False
        
    finally:
        sqlite_session.close()
        postgres_session.close()

if __name__ == "__main__":
    print("🚀 Starting database migration from SQLite to PostgreSQL...")
    print("=" * 50)
    
    success = migrate_sqlite_to_postgres()
    
    if success:
        print("=" * 50)
        print("✅ Migration completed successfully!")
        print("You can now deploy to Vercel with PostgreSQL database")
    else:
        print("=" * 50)
        print("❌ Migration failed!")
        print("Please check your DATABASE_URL and try again")