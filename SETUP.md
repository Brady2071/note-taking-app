# Local Setup and Testing Guide

## Prerequisites

- Python 3.8+ installed
- Node.js 16+ and npm installed
- Git installed

## Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Initialize database**:
   ```bash
   python init_db.py
   ```

6. **Start backend server**:
   ```bash
   python app.py
   ```

   Backend will run on http://localhost:5000

## Frontend Setup

1. **Open new terminal and navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm start
   ```

   Frontend will run on http://localhost:3000

## Testing the Application

### Manual Testing Checklist

1. **Create Note**:
   - Click "New Note" button
   - Enter title and content
   - Add tags (optional)
   - Click "Save" or press Ctrl+Enter
   - Verify note appears in sidebar

2. **Edit Note**:
   - Click on existing note in sidebar
   - Modify title, content, or tags
   - Save changes
   - Verify changes are reflected

3. **Delete Note**:
   - Click on note in sidebar
   - Click "Delete" button
   - Confirm deletion
   - Verify note is removed

4. **Search Notes**:
   - Use search bar to search by title or content
   - Verify only matching notes are shown
   - Clear search to show all notes

5. **Responsive Design**:
   - Resize browser window
   - Test on mobile view (F12 → Device toolbar)

### API Testing with curl

```bash
# Get all notes
curl http://localhost:5000/api/notes

# Create a note
curl -X POST http://localhost:5000/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Note", "content": "This is a test note", "tags": ["test"]}'

# Get specific note (replace 1 with actual ID)
curl http://localhost:5000/api/notes/1

# Update note
curl -X PUT http://localhost:5000/api/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Note", "content": "Updated content", "tags": ["updated"]}'

# Search notes
curl "http://localhost:5000/api/notes/search?q=test"

# Delete note
curl -X DELETE http://localhost:5000/api/notes/1
```

### Automated Testing

**Backend Test** (optional):
```bash
cd backend
pip install pytest
python -m pytest test_app.py -v
```

**Frontend Test**:
```bash
cd frontend
npm test
```

## Troubleshooting

### Backend Issues
- **Port 5000 in use**: Change port in `app.py` (line 67)
- **Database errors**: Delete `notes.db` and run `python init_db.py` again
- **CORS errors**: Ensure Flask-CORS is installed and configured

### Frontend Issues
- **Port 3000 in use**: React will automatically suggest another port
- **API connection errors**: Check if backend is running on port 5000
- **Build errors**: Delete `node_modules` and run `npm install` again

### Database Inspection

**Using VSCode**:
1. Install "SQLite Viewer" extension
2. Open `backend/notes.db` file
3. Browse tables and data

**Using command line**:
```bash
cd backend
sqlite3 notes.db
.tables
SELECT * FROM notes;
.quit
```

## Concurrent Edits Edge Case

To test concurrent edits:
1. Open two browser tabs/windows
2. Edit the same note in both
3. Save in both tabs
4. Verify the last save wins (expected behavior)

## Performance Notes

- SQLite database file is created in `backend/` directory
- Database grows with note count (no automatic cleanup)
- Search is case-insensitive and searches both title and content
- No pagination implemented (may be slow with many notes)
