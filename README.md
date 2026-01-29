# arxiv-organizer

[![PyPI version](https://badge.fury.io/py/arxiv-organizer.svg)](https://badge.fury.io/py/arxiv-organizer)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/arxiv-organizer)](https://pepy.tech/project/arxiv-organizer)

> **Organize your academic research library with AI-powered intelligence.**

Transform your chaotic paper downloads into a beautifully organized, searchable research library. `arxiv-organizer` automatically downloads, categorizes, and enriches arXiv papers using Google's Gemini AI - or works perfectly without any AI at all.

## Features

### Core Organization (v1.0)
- **Automatic Renaming**: Renames files to `Author_Title_ID.pdf` for easy identification.
- **Smart Categorization**: Sorts papers into folders based on their primary arXiv category (e.g., `cs/Artificial Intelligence`).
- **Parallel Processing**: Uses multi-threading to organize large collections in seconds.
- **Metadata Sidecars**: Generates a JSON sidecar for each paper containing full metadata (abstract, authors, DOI, etc.).
- **Local Library Index**: Maintains a `library.json` index of your collection to enable smart updates and fast lookups.
- **Progress Tracking**: Shows a progress bar during processing.

### Auto-Download (v2.0)
- **Query Builder**: Search by keywords, title, abstract, or raw arXiv query syntax.
- **Time Filters**: Download papers from the last day, week, month, 3 months, year, 3/5/10/20/30 years, or all time.
- **Smart Judge (AI)**: Use Gemini Flash Lite to filter papers based on natural language criteria (e.g., "Papers about LLM reasoning, excluding surveys").

### Smart Organization (v2.0)
- **AI Classification**: Classify papers into *your* custom topics (e.g., "Agents", "RAG", "Multimodal") using Gemini, instead of just arXiv categories.
- **AI Enrichment**: Add AI-generated summaries and tags to the metadata sidecars for each paper.

## Installation

You can install `arxiv-organizer` directly from PyPI:

```bash
pip install arxiv-organizer
```

Or install from source:

```bash
git clone https://github.com/mozayed007/arxiv-organizer.git
cd arxiv-organizer
pip install -r requirements.txt
pip install .
```

## Configuration

### AI Features (Optional)

**All AI features are completely optional.** The package works perfectly without any configuration.

To enable AI features (Smart Judge, Smart Organization, AI Enrichment):

1. Get a free Google API key: https://aistudio.google.com/app/apikey
2. Create a `.env` file in your working directory:

```bash
GOOGLE_API_KEY=your_api_key_here
```

3. Use the corresponding CLI flags when running

**Without API key**: Package falls back to standard organization by arXiv categories.

**See [PIPELINE.md](docs/PIPELINE.md) for detailed documentation on how AI features degrade gracefully.**

## Usage

### Basic Organization

Navigate to the directory containing your downloaded arXiv PDFs and run:

```bash
arxiv-organizer
```

### Download Papers

Download the latest 10 papers about "reinforcement learning":

```bash
arxiv-organizer --download --keywords "reinforcement learning" --period 30d --max 10
```

Download papers with Smart Judge filtering:

```bash
arxiv-organizer --download \
  --keywords "large language models" \
  --period 7d \
  --max 20 \
  --smart-judge \
  --judge-criteria "Papers about LLM reasoning capabilities, exclude surveys and benchmarks"
```

### Smart Organization

Organize your papers with AI classification into custom topics:

```bash
arxiv-organizer --smart-organize --custom-topics "Agents,RAG,Multimodal,Reasoning,FineTuning"
```

### Combined Workflow

Download and organize in one command:

```bash
arxiv-organizer --download \
  --keywords "computer vision" \
  --period 90d \
  --max 50 \
  --smart-judge \
  --judge-criteria "Novel architectures for object detection" \
  --smart-organize \
  --custom-topics "Detection,Segmentation,3D Vision"
```

### CLI Reference

```
# Download Options
--download          Enable download mode
--keywords          Comma-separated keywords to search in all fields
--title-keywords    Comma-separated keywords to search in titles
--abstract-keywords Comma-separated keywords to search in abstracts
--period            Time period: 1d, 7d, 30d, 90d, 1y, 3y, 5y, 10y, 20y, 30y, all (default: all)
--max               Maximum papers to download (default: 10)
--smart-judge       Enable Gemini-based filtering
--judge-criteria    Natural language criteria for Smart Judge

# Organization Options
--smart-organize    Enable AI-based organization and enrichment
--custom-topics     Comma-separated custom topics for AI classification
```

## How it Works

1. **Download (Optional)**: Queries arXiv API, filters by date and criteria (optionally using AI), downloads PDFs.
2. **Scan**: Finds PDF files matching the arXiv ID pattern (e.g., `2101.00001.pdf`).
3. **Fetch**: Retrieves metadata from the arXiv API.
4. **Enrich (Optional)**: Uses Gemini to generate summaries, tags, and classify into custom topics.
5. **Rename**: Renames the file to a readable format.
6. **Move**: Organizes the file into a structured folder hierarchy.
7. **Index**: Creates a `{filename}.json` sidecar and updates `library.json`.

## File Structure

After organization, your directory will look like:

```
your_directory/
├── arxiv/
│   ├── library.json                          # Master index
│   ├── Smart_Topics/                         # AI-classified papers (if using --smart-organize)
│   │   ├── Agents/
│   │   │   ├── Smith_AttentionIs_2301.12345.pdf
│   │   │   └── Smith_AttentionIs_2301.12345.json
│   │   └── RAG/
│   ├── cs/                                   # arXiv category-based organization
│   │   ├── Artificial Intelligence/
│   │   ├── Computer Vision/
│   │   └── ...
│   └── ...
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)

## Author

**MoZayed** - [GitHub](https://github.com/mozayed007) | [LinkedIn](https://linkedin.com/in/mozayed007)

## Support

If you find this tool useful, please:
- ⭐ Star the repository
- 🐛 Report bugs via [Issues](https://github.com/mozayed007/arxiv-organizer/issues)
- 💡 Suggest features via [Discussions](https://github.com/mozayed007/arxiv-organizer/discussions)
- 📢 Share with your research community

## Roadmap

- [ ] Vector search over the library using embeddings
- [ ] Integration with local LLM chat interfaces (llama.cpp, etc.)
- [ ] Web UI for browsing and searching your library
- [ ] Export to reference managers (Zotero, Mendeley)
- [ ] Citation graph visualization
- [ ] Duplicate detection across your library

---

<div align="center">
Made with ❤️ for researchers, by researchers.
</div>
