# Note-Taking Web App

A minimal note-taking web application built with React + TypeScript frontend and Flask + Python backend.

## Project Structure

```
note-app/
├── backend/
│   ├── app.py                 # Flask application
│   ├── models.py              # SQLAlchemy models
│   ├── requirements.txt       # Python dependencies
│   └── init_db.py            # Database initialization
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── services/          # API services
│   │   ├── types/             # TypeScript types
│   │   └── App.tsx
│   ├── package.json
│   └── tsconfig.json
├── .gitignore
└── README.md
```

## Quick Start

1. **Backend Setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python init_db.py
   python app.py
   ```

2. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Access**: Open http://localhost:3000

## API Endpoints

- `GET /api/notes` - List all notes
- `POST /api/notes` - Create note
- `GET /api/notes/<id>` - Get note by ID
- `PUT /api/notes/<id>` - Update note
- `DELETE /api/notes/<id>` - Delete note
- `GET /api/notes/search?q=...` - Search notes
