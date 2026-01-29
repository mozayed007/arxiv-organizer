# ArXiv Organizer - Complete Pipeline Documentation

## Table of Contents
1. [Pipeline Overview](#pipeline-overview)
2. [AI Features (Optional)](#ai-features-optional)
3. [Usage Examples](#usage-examples)
4. [Configuration](#configuration)
5. [Troubleshooting](#troubleshooting)

## Pipeline Overview

The `arxiv-organizer` has two main workflows that can be used independently or together:

### Workflow 1: Download → Organize
```
User Input (CLI) → Download Phase → Organize Phase → Structured Library
```

### Workflow 2: Organize Existing PDFs
```
User Input (CLI) → Organize Phase → Structured Library
```

### Detailed Pipeline Steps

#### Phase 1: Download (Optional - requires `--download` flag)
1. **Query Construction**:
   - Combines `--query`, `--keywords`, `--title-keywords`, `--abstract-keywords`
   - Builds valid arXiv API query string
   
2. **Fetch from arXiv**:
   - Searches arXiv API with constructed query
   - Fetches 2x `--max` results for filtering buffer
   
3. **Date Filtering**:
   - Filters papers based on `--period` (1d, 7d, 30d, 1y, etc.)
   - Uses paper's `published` date
   
4. **Smart Judge (Optional AI - requires `--smart-judge` and API key)**:
   - Sends paper titles + abstracts to Gemini
   - Filters based on `--judge-criteria` (natural language)
   - Falls back gracefully if no API key
   
5. **Download PDFs**:
   - Downloads papers to `--directory`
   - Filename format: `{arxiv_id}.pdf` (e.g., `2301.12345.pdf`)
   - Shows progress bar
   - Skips already downloaded files

#### Phase 2: Organize (Always runs if PDFs exist)
1. **Scan Directory**:
   - Finds all PDFs matching arXiv ID pattern: `\d{4}\.\d{5}(v\d+)?\.pdf`
   - Checks `library.json` index
   - Skips already indexed papers (smart updates)
   
2. **Fetch Metadata** (Parallel):
   - Uses ThreadPoolExecutor (5 workers)
   - Queries arXiv API for each paper
   - Creates PaperMetadata objects
   
3. **AI Enrichment (Optional - requires `--smart-organize` and API key)**:
   - **Classification**: Assigns paper to custom topic (e.g., "Agents", "RAG")
   - **Summary**: Generates 1-sentence AI summary
   - **Tags**: Generates 3-5 relevant tags
   - Falls back to standard organization if no API key
   
4. **Rename**:
   - Format: `{Author}_{TitleWords}_{ArxivID}.pdf`
   - Example: `Smith_AttentionIsAll_2301.12345.pdf`
   
5. **Organize into Folders**:
   - **Priority 1** (if `--smart-organize` enabled): `Smart_Topics/{CustomTopic}/`
   - **Priority 2**: `{MainCategory}/{Subcategory}/` (arXiv categories)
   - Example: `arxiv/cs/Artificial Intelligence/`
   
6. **Create Metadata Sidecar**:
   - JSON file: `{filename}.json`
   - Contains: title, authors, abstract, categories, DOI, PDF URL
   - **If AI enabled**: Also includes `ai_summary`, `ai_tags`, `custom_topic`
   
7. **Update Library Index**:
   - Updates `arxiv/library.json` with all papers
   - Enables fast lookups and smart updates

## AI Features (Optional)

### Activation Requirements

AI features are **completely optional** and require:
1. A `.env` file with `GOOGLE_API_KEY=your_key`
2. Explicit CLI flags (`--smart-judge` or `--smart-organize`)

### Breakdown by Feature

| Feature | Requires | Description | Fallback Behavior |
|---------|----------|-------------|-------------------|
| Smart Judge | `--smart-judge` + API key | Filter downloads by natural language criteria | Returns all papers if no API key |
| AI Classification | `--smart-organize` + API key | Classify into custom topics | Uses arXiv categories |
| AI Summary | `--smart-organize` + API key | Generate 1-sentence summary | Skipped, field is `null` |
| AI Tags | `--smart-organize` + API key | Generate relevant tags | Skipped, field is `null` |

### How Optionality Works

The `GeminiClient` class is designed to gracefully degrade:

```python
class GeminiClient:
    def __init__(self, api_key: str):
        if not api_key:
            self.logger.warning("No API key. AI features disabled.")
            self.model = None  # Marks as non-functional
```

- **No API key**: Client logs warning, all methods return defaults
- **Invalid API key**: Client logs error, all methods return defaults
- **All features**: Methods check `if self.model` before making API calls

### Example: No API Key Behavior

```bash
# User runs with AI features but no API key
arxiv-organizer --smart-organize --custom-topics "Agents,RAG"

# Logs show:
# WARNING: Google API Key not provided. AI features will not be available.
# INFO: Processing papers...
# INFO: Organization complete.

# Result: Papers organized by arXiv categories (fallback)
```

## Usage Examples

### 1. Basic Organization (No AI)
```bash
# Organize existing PDFs in current directory
arxiv-organizer

# Organize PDFs in specific directory
arxiv-organizer --directory /path/to/papers
```

**Pipeline**: Scan → Fetch Metadata → Rename → Organize by arXiv categories → Index

### 2. Download Only (No AI)
```bash
# Download latest 10 NLP papers from last 30 days
arxiv-organizer --download \
  --keywords "natural language processing" \
  --period 30d \
  --max 10
```

**Pipeline**: Query → Fetch → Date Filter → Download → Organize by arXiv categories

### 3. Download with Smart Judge (AI)
```bash
# Download LLM papers, but only about reasoning
arxiv-organizer --download \
  --keywords "large language models" \
  --period 7d \
  --max 20 \
  --smart-judge \
  --judge-criteria "Papers about LLM reasoning and planning capabilities, exclude benchmark papers"
```

**Pipeline**: Query → Fetch → Date Filter → **AI Judge** → Download → Organize by arXiv categories

### 4. Smart Organization (AI)
```bash
# Organize existing papers into custom topics with AI
arxiv-organizer --smart-organize \
  --custom-topics "Agents,RAG,Multimodal,FineTuning,Reasoning"
```

**Pipeline**: Scan → Fetch Metadata → **AI Classify** → **AI Enrich** → Rename → Organize by custom topics → Index

### 5. Full AI Pipeline
```bash
# Download + Smart Judge + Smart Organization
arxiv-organizer --download \
  --keywords "computer vision" \
  --period 90d \
  --max 50 \
  --smart-judge \
  --judge-criteria "Novel architectures for object detection and segmentation" \
  --smart-organize \
  --custom-topics "Object Detection,Segmentation,3D Vision"
```

**Pipeline**: Query → Fetch → Date Filter → **AI Judge** → Download → Scan → **AI Classify** → **AI Enrich** → Organize by custom topics → Index

## Configuration

### Environment Variables (.env file)

Create a `.env` file in your working directory:

```bash
# Required for AI features only
GOOGLE_API_KEY=your_google_api_key_here
```

**Get API Key**: https://aistudio.google.com/app/apikey

### Directory Structure Output

After running with `--smart-organize`:

```
your_directory/
├── .env                                   # Your config (optional)
├── 2301.12345.pdf                         # Original downloaded PDF
├── 2301.12346.pdf
├── arxiv/
│   ├── library.json                       # Master index of all papers
│   ├── Smart_Topics/                      # AI-classified papers
│   │   ├── Agents/
│   │   │   ├── Smith_AttentionIs_2301.12345.pdf
│   │   │   └── Smith_AttentionIs_2301.12345.json  # Metadata with AI fields
│   │   ├── RAG/
│   │   │   ├── Johnson_Retrieval_2302.54321.pdf
│   │   │   └── Johnson_Retrieval_2302.54321.json
│   │   └── Unclassified/                  # Falls back if unclear
│   └── cs/                                # Standard arXiv categories (if no AI)
│       ├── Artificial Intelligence/
│       ├── Computer Vision/
│       └── ...
```

## Troubleshooting

### Issue: AI features not working

**Symptoms**: Papers organized by arXiv categories despite using `--smart-organize`

**Solutions**:
1. Check `.env` file exists and contains `GOOGLE_API_KEY=...`
2. Verify API key is valid: https://aistudio.google.com/app/apikey
3. Check logs for warning: "Google API Key not provided"

### Issue: Download but no organization

**Cause**: Downloaded PDFs are in the directory, but organizer didn't run

**Solution**: Make sure you're not using `--download` with criteria that return 0 papers. Check logs.

### Issue: Smart Judge returns all papers

**Cause**: No API key or API error

**Solution**: 
- Check `.env` file
- Review logs for Gemini API errors
- Verify `--judge-criteria` is provided

### Issue: Papers not re-organized on second run

**Explanation**: This is expected behavior. The `library.json` index tracks organized papers. Delete the index to re-process:

```bash
rm arxiv/library.json
arxiv-organizer --smart-organize --custom-topics "NewTopics"
```

## Summary

- **AI features are optional**: Package works perfectly without any API keys
- **Graceful degradation**: If AI is requested but unavailable, falls back to standard behavior
- **Coherent pipeline**: Download → Organize works seamlessly
- **Smart updates**: Won't re-process already organized papers
- **Rich metadata**: Every paper gets a JSON sidecar with full metadata
