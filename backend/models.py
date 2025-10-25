from datetime import datetime
import json
import os

# Try to import SQLAlchemy, fallback if not available
try:
    from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Time, create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False
    print("SQLAlchemy not available, database features disabled")

if SQLALCHEMY_AVAILABLE:
    Base = declarative_base()

    class Note(Base):
        __tablename__ = 'notes'
        
        id = Column(Integer, primary_key=True)
        title = Column(String(200), nullable=False)
        content = Column(Text, nullable=False)
        tags = Column(Text)  # JSON string of tags array
        event_date = Column(Date, nullable=True)  # Optional event date
        event_time = Column(Time, nullable=True)  # Optional event time
        updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        def to_dict(self):
            return {
                'id': self.id,
                'title': self.title,
                'content': self.content,
                'tags': json.loads(self.tags) if self.tags else [],
                'eventDate': self.event_date.isoformat() if self.event_date else None,
                'eventTime': self.event_time.isoformat() if self.event_time else None,
                'updatedAt': self.updated_at.isoformat()
            }
        
        @classmethod
        def from_dict(cls, data):
            note = cls()
            note.title = data.get('title', '')
            note.content = data.get('content', '')
            note.tags = json.dumps(data.get('tags', []))
            return note

    # Database setup - supports both local SQLite and production Postgres
    def get_database_url():
        """Get database URL from environment variable or default to SQLite"""
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            # Convert postgresql:// to postgresql+pg8000:// for pg8000 driver
            if database_url.startswith('postgresql://'):
                database_url = database_url.replace('postgresql://', 'postgresql+pg8000://')
            return database_url
        else:
            return 'sqlite:///notes.db'

    try:
        engine = create_engine(get_database_url(), echo=False)
        Base.metadata.create_all(engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    except Exception as e:
        print(f"Database setup failed: {e}")
        engine = None
        SessionLocal = None
else:
    # Fallback classes when SQLAlchemy is not available
    class Note:
        def __init__(self):
            self.id = None
            self.title = ""
            self.content = ""
            self.tags = "[]"
            self.event_date = None
            self.event_time = None
            self.updated_at = datetime.utcnow()
        
        def to_dict(self):
            return {
                'id': self.id,
                'title': self.title,
                'content': self.content,
                'tags': json.loads(self.tags) if self.tags else [],
                'eventDate': self.event_date.isoformat() if self.event_date else None,
                'eventTime': self.event_time.isoformat() if self.event_time else None,
                'updatedAt': self.updated_at.isoformat()
            }
        
        @classmethod
        def from_dict(cls, data):
            note = cls()
            note.title = data.get('title', '')
            note.content = data.get('content', '')
            note.tags = json.dumps(data.get('tags', []))
            return note
    
    engine = None
    SessionLocal = None
