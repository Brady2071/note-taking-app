export interface Note {
  id: number;
  title: string;
  content: string;
  tags: string[];
  eventDate?: string;
  eventTime?: string;
  updatedAt: string;
}

export interface CreateNoteRequest {
  title: string;
  content: string;
  tags?: string[];
}

export interface UpdateNoteRequest {
  title?: string;
  content?: string;
  tags?: string[];
  eventDate?: string;
  eventTime?: string;
}

export interface TranslateRequest {
  targetLang: string;
}

export interface TranslateResponse {
  title: string;
  content: string;
  originalId?: number;
}

export interface GenerateNoteRequest {
  input: string;
  language?: string;
}
