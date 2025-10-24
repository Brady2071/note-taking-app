import os
import json
import time
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class LLMResponse:
    content: str
    usage: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv('GITHUB_TOKEN')
        self.base_url = "https://models.github.ai/inference"
        self.model = "openai/gpt-4.1-mini"
        
        if not self.api_key:
            raise ValueError("GITHUB_TOKEN environment variable is required")
    
    def call_llm_model(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 1.0, 
        top_p: float = 1.0,
        max_retries: int = 3,
        backoff_factor: float = 2.0
    ) -> LLMResponse:
        """
        Call GitHub Models inference endpoint with retry logic and rate limiting
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": 2000
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.base_url,
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return LLMResponse(
                        content=data.get('choices', [{}])[0].get('message', {}).get('content', ''),
                        usage=data.get('usage', {})
                    )
                elif response.status_code == 429:  # Rate limit
                    wait_time = backoff_factor ** attempt
                    print(f"Rate limited. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    return LLMResponse(
                        content="",
                        error=f"API error: {response.status_code} - {response.text}"
                    )
                    
            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    return LLMResponse(
                        content="",
                        error=f"Request failed: {str(e)}"
                    )
                wait_time = backoff_factor ** attempt
                time.sleep(wait_time)
        
        return LLMResponse(
            content="",
            error="Max retries exceeded"
        )

def translate_text(
    text: str, 
    target_language: str, 
    title: Optional[str] = None
) -> Dict[str, str]:
    """
    Translate text using GitHub Models
    Returns: {title: str, content: str}
    """
    client = LLMClient()
    
    system_prompt = f"""You are a professional translator. Translate the following text to {target_language}.
    
    Rules:
    1. Preserve the original meaning and style
    2. If a title is provided, translate it concisely (≤5 words)
    3. If no title is provided, generate a concise title (≤5 words) in {target_language}
    4. Return ONLY a JSON object with "title" and "content" fields
    5. Do not include any other text or explanations
    
    Example response format:
    {{"title": "Translated Title", "content": "Translated content here..."}}"""
    
    user_prompt = f"Title: {title or 'None'}\nContent: {text}"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    response = client.call_llm_model(messages, temperature=0.3)
    
    if response.error:
        raise Exception(f"Translation failed: {response.error}")
    
    try:
        result = json.loads(response.content)
        return {
            "title": result.get("title", ""),
            "content": result.get("content", "")
        }
    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        return {
            "title": title or "Translated Note",
            "content": response.content
        }

def generate_structured_notes(
    user_input: str, 
    language: str = "en"
) -> Dict[str, Any]:
    """
    Generate structured notes from natural language input
    Returns: {title, content, tags, event_date, event_time}
    """
    client = LLMClient()
    
    system_prompt = f"""You are a helpful assistant that creates structured notes from natural language descriptions.
    
    Rules:
    1. Generate a clear, concise title (≤10 words)
    2. Create detailed, well-organized content
    3. Suggest 2-4 relevant tags
    4. If the input mentions a date/time, extract it
    5. Return ONLY a JSON object with these fields:
       - title: string
       - content: string  
       - tags: array of strings
       - event_date: string (YYYY-MM-DD format or null)
       - event_time: string (HH:MM format or null)
    
    Example response:
    {{"title": "Meeting Notes", "content": "Detailed content...", "tags": ["work", "meeting"], "event_date": "2024-01-15", "event_time": "14:30"}}"""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Create a note from: {user_input}"}
    ]
    
    response = client.call_llm_model(messages, temperature=0.7)
    
    if response.error:
        raise Exception(f"Note generation failed: {response.error}")
    
    try:
        result = json.loads(response.content)
        return {
            "title": result.get("title", "Generated Note"),
            "content": result.get("content", user_input),
            "tags": result.get("tags", []),
            "event_date": result.get("event_date"),
            "event_time": result.get("event_time")
        }
    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        return {
            "title": "Generated Note",
            "content": user_input,
            "tags": ["generated"],
            "event_date": None,
            "event_time": None
        }
