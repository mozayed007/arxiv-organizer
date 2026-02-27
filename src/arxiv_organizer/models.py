from pydantic import BaseModel, Field, AwareDatetime
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional, Dict
from datetime import datetime

class GlobalConfig(BaseSettings):
    google_api_key: Optional[str] = Field(None, description="Google API Key for Gemini")
    
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

class PaperMetadata(BaseModel):
    id: str
    title: str
    authors: List[str]
    summary: str
    published: AwareDatetime
    updated: AwareDatetime
    primary_category: str
    categories: List[str]
    pdf_url: str
    doi: Optional[str] = None
    
    # Smart features
    ai_summary: Optional[str] = None
    ai_tags: Optional[List[str]] = None
    custom_topic: Optional[str] = None

class DownloadConfig(BaseModel):
    query: Optional[str] = None
    keywords: Optional[List[str]] = None
    title_keywords: Optional[List[str]] = None
    abstract_keywords: Optional[List[str]] = None
    period: str = "all"
    max_results: int = 10
    smart_judge: bool = False
    judge_criteria: Optional[str] = None
    download_dir: str = "."

class OrganizerConfig(BaseModel):
    base_dir: str
    smart_organize: bool = False
    custom_topics: Optional[List[str]] = None
