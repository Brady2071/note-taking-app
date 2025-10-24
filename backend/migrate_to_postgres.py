#!/usr/bin/env python3
"""
Migration script to move from SQLite to Postgres/Supabase
Run this script to migrate existing data to the new database
"""

import os
import json
from datetime import datetime, date, time
from sqlalchemy import create_engine, text
from models import Base, Note, SessionLocal
from dotenv import load_dotenv

load_dotenv()

def migrate_data():
    """Migrate data from SQLite to Postgres"""
    
    # Source database (SQLite)
    sqlite_engine = create_engine('sqlite:///notes.db', echo=False)
    sqlite_session = sessionmaker(autocommit=False, autoflush=False, bind=sqlite_engine)()
    
    # Target database (Postgres)
    postgres_url = os.getenv('DATABASE_URL')
    if not postgres_url:
        print("DATABASE_URL not found. Please set it in your environment.")
        return
    
    postgres_engine = create_engine(postgres_url, echo=False)
    postgres_session = sessionmaker(autocommit=False, autoflush=False, bind=postgres_engine)()
    
    try:
        # Create tables in Postgres
        Base.metadata.create_all(postgres_engine)
        print("Created tables in Postgres database")
        
        # Get all notes from SQLite
        old_notes = sqlite_session.query(Note).all()
        print(f"Found {len(old_notes)} notes to migrate")
        
        # Migrate each note
        for old_note in old_notes:
            new_note = Note(
                title=old_note.title,
                content=old_note.content,
                tags=old_note.tags,
                event_date=None,  # New field, set to None for existing notes
                event_time=None,  # New field, set to None for existing notes
                updated_at=old_note.updated_at
            )
            postgres_session.add(new_note)
        
        postgres_session.commit()
        print(f"Successfully migrated {len(old_notes)} notes to Postgres")
        
        # Verify migration
        new_notes = postgres_session.query(Note).all()
        print(f"Verification: {len(new_notes)} notes now in Postgres database")
        
    except Exception as e:
        postgres_session.rollback()
        print(f"Migration failed: {e}")
    finally:
        sqlite_session.close()
        postgres_session.close()

if __name__ == '__main__':
    migrate_data()
