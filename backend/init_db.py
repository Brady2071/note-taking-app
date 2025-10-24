from models import Base, engine, SessionLocal, Note
import json

def init_database():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create sample data
    db = SessionLocal()
    try:
        # Check if notes already exist
        if db.query(Note).count() == 0:
            sample_notes = [
                {
                    'title': 'Welcome to Note App',
                    'content': 'This is your first note. You can edit, delete, and search through your notes.',
                    'tags': ['welcome', 'getting-started']
                },
                {
                    'title': 'Meeting Notes',
                    'content': 'Project discussion:\n- Review requirements\n- Set deadlines\n- Assign tasks',
                    'tags': ['work', 'meeting']
                },
                {
                    'title': 'Shopping List',
                    'content': '- Milk\n- Bread\n- Eggs\n- Coffee',
                    'tags': ['personal', 'shopping']
                }
            ]
            
            for note_data in sample_notes:
                note = Note()
                note.title = note_data['title']
                note.content = note_data['content']
                note.tags = json.dumps(note_data['tags'])
                db.add(note)
            
            db.commit()
            print("Database initialized with sample data!")
        else:
            print("Database already contains data.")
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    init_database()
