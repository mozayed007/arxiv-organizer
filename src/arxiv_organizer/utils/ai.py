import google.generativeai as genai
from typing import List, Dict
import logging
import json
import time
from ..models import PaperMetadata

class RateLimiter:
    def __init__(self, calls_per_minute: int = 15):
        self.interval = 60.0 / calls_per_minute
        self.last_call = 0.0

    def wait(self):
        now = time.time()
        elapsed = now - self.last_call
        if elapsed < self.interval:
            time.sleep(self.interval - elapsed)
        self.last_call = time.time()

class GeminiClient:
    def __init__(self, api_key: str):
        self.logger = logging.getLogger(__name__)
        self.rate_limiter = RateLimiter(calls_per_minute=15) # ~1 call every 4s
        
        if not api_key:
            self.logger.warning("Google API Key not provided. AI features will not be available.")
            self.model = None
            return
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-lite-preview-02-05')
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini: {e}")
            self.model = None

    def judge_papers(self, papers: List[PaperMetadata], criteria: str) -> List[str]:
        """
        Returns a list of paper IDs that match the criteria.
        """
        if not self.model:
            self.logger.warning("Gemini model not available. Returning all papers.")
            return [p.id for p in papers]
            
        if not papers:
            return []

        # Batch processing for judge could be added here if list is huge
        # For now, we assume reasonable batch sizes or single call
        self.rate_limiter.wait()

        prompt = f"""
        You are a research assistant. I will provide a list of academic papers (ID, Title, Abstract).
        Your task is to select the papers that match the following criteria: "{criteria}"
        
        Return ONLY a JSON list of the IDs of the selected papers. If none match, return an empty list [].
        
        Papers:
        """
        
        for p in papers:
            prompt += f"- ID: {p.id}\n  Title: {p.title}\n  Abstract: {p.summary[:500]}...\n\n"

        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            # Clean up markdown code blocks if present
            if text.startswith("```json"):
                text = text[7:-3]
            elif text.startswith("```"):
                text = text[3:-3]
            
            selected_ids = json.loads(text)
            return selected_ids
        except Exception as e:
            self.logger.error(f"Gemini Judge failed: {e}")
            return []

    def analyze_paper(self, paper: PaperMetadata, topics: List[str] = None) -> Dict:
        """
        Performs both classification and enrichment in a single API call to save rate limits.
        """
        if not self.model:
            return {}
            
        self.rate_limiter.wait()
        
        topics_str = ', '.join(topics) if topics else "General"
        
        prompt = f"""
        Analyze this paper.
        1. Classify it into exactly ONE of these topics: {topics_str}. If none match well or no topics provided, use "Unclassified".
        2. Provide a 1-sentence summary.
        3. Provide 3-5 relevant tags.
        
        Return JSON format: 
        {{ 
            "topic": "TopicName",
            "summary": "One sentence summary...", 
            "tags": ["tag1", "tag2"] 
        }}
        
        Title: {paper.title}
        Abstract: {paper.summary[:1500]}
        """
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:-3]
            elif text.startswith("```"):
                text = text[3:-3]
            return json.loads(text)
        except Exception as e:
            self.logger.error(f"Gemini Analysis failed: {e}")
            return {}

