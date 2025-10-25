import { Note, CreateNoteRequest, UpdateNoteRequest, TranslateRequest, TranslateResponse, GenerateNoteRequest } from '../types/Note';

const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

class ApiService {
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async getNotes(): Promise<Note[]> {
    return this.request<Note[]>('/notes');
  }

  async getNote(id: number): Promise<Note> {
    return this.request<Note>(`/notes/${id}`);
  }

  async createNote(note: CreateNoteRequest): Promise<Note> {
    return this.request<Note>('/notes', {
      method: 'POST',
      body: JSON.stringify(note),
    });
  }

  async updateNote(id: number, note: UpdateNoteRequest): Promise<Note> {
    return this.request<Note>(`/notes/${id}`, {
      method: 'PUT',
      body: JSON.stringify(note),
    });
  }

  async deleteNote(id: number): Promise<void> {
    await this.request(`/notes/${id}`, {
      method: 'DELETE',
    });
  }

  async searchNotes(query: string): Promise<Note[]> {
    return this.request<Note[]>(`/notes/search?q=${encodeURIComponent(query)}`);
  }

  async translateNote(id: number, request: TranslateRequest): Promise<TranslateResponse> {
    return this.request<TranslateResponse>(`/notes/${id}/translate`, {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async translateText(request: TranslateRequest & { title?: string; content: string }): Promise<TranslateResponse> {
    return this.request<TranslateResponse>('/translate', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async generateNote(request: GenerateNoteRequest): Promise<Note> {
    return this.request<Note>('/generate-note', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }
}

export const apiService = new ApiService();
