# Release Notes

## Version 2.0.0 (2025-11-20)

### 🚀 Major Release: AI-Powered Research Library Management

This release transforms `arxiv-organizer` from a simple categorization tool into an intelligent research assistant powered by Google's Gemini AI.

### ✨ New Features

#### Auto-Downloader
- **Smart Download**: Query arXiv by keywords, title, or abstract
- **Time Filters**: Download papers from last day/week/month/year (up to 30 years)
- **Flexible Queries**: Support for raw arXiv query syntax
- **Progress Tracking**: Visual progress bars for all operations

#### AI-Powered Features (Optional)
- **Smart Judge**: Filter downloads using natural language criteria
  - Example: "Papers about LLM reasoning, excluding surveys"
- **AI Classification**: Organize papers into *your* custom topics
  - Example: Classify into "Agents", "RAG", "Multimodal" instead of arXiv categories
- **AI Enrichment**: Auto-generate summaries and tags for each paper
- **Graceful Degradation**: Works perfectly without AI - just uses arXiv categories

#### Enhanced Organization
- **Pydantic Integration**: Robust type safety and validation
- **Configuration Management**: Support for `.env` files
- **Smart Updates**: Skip already-processed papers automatically
- **Rich Metadata**: JSON sidecars with complete paper information

### 🔧 Technical Improvements
- Thread-safe parallel processing
- Comprehensive error handling
- Modular, testable architecture
- Type hints throughout

### 📚 Documentation
- Complete pipeline documentation ([PIPELINE.md](PIPELINE.md))
- Usage examples for all modes
- Troubleshooting guide
- `.env.example` template

### 📦 Installation
```bash
pip install arxiv-organizer==2.0.0
```

### 🎯 Usage Examples

**Download latest ML papers:**
```bash
arxiv-organizer --download --keywords "machine learning" --period 7d --max 10
```

**Smart organization with AI:**
```bash
arxiv-organizer --smart-organize --custom-topics "Agents,RAG,Multimodal"
```

**Full pipeline:**
```bash
arxiv-organizer --download \
  --keywords "LLM" \
  --smart-judge \
  --judge-criteria "Papers about reasoning" \
  --smart-organize \
  --custom-topics "Reasoning,Planning"
```

### 🔄 Migration from v1.x

No breaking changes! v2.0 is backward compatible. All v1.x commands work exactly the same.

New features are opt-in via CLI flags.

### 🙏 Credits

Thanks to all contributors and users who provided feedback!

---

## Version 0.2.0 (Previous)

- Parallel processing with ThreadPoolExecutor
- Progress bars with tqdm
- Metadata sidecar files
- Local library index (library.json)

## Version 0.1.0 (Initial)

- Basic PDF organization by arXiv category
- Automatic renaming
- Category-based folder structure
