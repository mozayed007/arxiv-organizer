# Usage Examples - Directory Handling

## Understanding Directory Structure

When you run `arxiv-organizer`, it works in a specific directory that contains:
1. Downloaded PDFs (named like `2301.12345.pdf`)
2. An `arxiv/` subdirectory where organized papers go

## Using `--directory` Flag

### Absolute Path (Recommended)
```bash
# Organize papers in a specific directory
arxiv-organizer --directory /home/user/research/papers

# Download and organize in a test directory
arxiv-organizer --download \
  --keywords "test" \
  --period 7d \
  --max 5 \
  --directory /home/user/test_papers
```

### Relative Path
```bash
# Organize papers in a subdirectory relative to current location
arxiv-organizer --directory ./my_papers

# From anywhere, organize papers in your home directory
arxiv-organizer --directory ~/Downloads/arxiv_papers
```

### Default (Current Directory)
```bash
# If no --directory is specified, uses current directory
cd /path/to/papers
arxiv-organizer
```

## Complete Workflow Example

### Setup Test Directory
```bash
# Create a test directory
mkdir -p ~/arxiv_test

# Download papers there
arxiv-organizer --download \
  --keywords "machine learning" \
  --period 30d \
  --max 10 \
  --directory ~/arxiv_test

# Papers are downloaded to: ~/arxiv_test/2301.12345.pdf, etc.
```

### Organize
```bash
# Organize the downloaded papers
arxiv-organizer --directory ~/arxiv_test

# Or combine download + organize in one command
arxiv-organizer --download \
  --keywords "NLP" \
  --period 7d \
  --max 5 \
  --directory ~/arxiv_test
```

### Result Structure
```
~/arxiv_test/
├── arxiv/                          # Organized papers go here
│   ├── library.json                # Index
│   ├── cs/
│   │   ├── Artificial Intelligence/
│   │   │   ├── Smith_Attention_2301.12345.pdf
│   │   │   └── Smith_Attention_2301.12345.json
│   │   └── Computation and Language/
│   └── stat/
└── [Any remaining unorganized PDFs stay in root]
```

## Directory Behavior

1. **Download**: PDFs go to `--directory` (or current dir)
2. **Organize**: Scans `--directory` for arXiv PDFs, moves them to `--directory/arxiv/`
3. **Smart Updates**: Won't re-organize papers already in `arxiv/`

## Testing with Different Directories

### Test 1: Basic Organization
```bash
# Create test directory and add some PDFs
mkdir test_org
cd test_org
# (manually place some arXiv PDFs here, e.g., 2301.12345.pdf)
arxiv-organizer
```

### Test 2: Download to Specific Location
```bash
arxiv-organizer --download \
  --keywords "computer vision" \
  --period 7d \
  --max 3 \
  --directory /tmp/arxiv_test
```

### Test 3: Smart Organization in Test Dir
```bash
arxiv-organizer \
  --directory ./research_papers \
  --smart-organize \
  --custom-topics "Agents,RAG,Multimodal"
```

## Path Resolution

The tool automatically resolves paths:
- `./papers` → `/current/working/dir/papers`
- `~/papers` → `/home/username/papers`
- `/absolute/path` → `/absolute/path`

## Common Patterns

### Separate Download and Organization
```bash
# Download only
arxiv-organizer --download \
  --keywords "physics" \
  --period 30d \
  --max 20 \
  --directory ~/downloads/arxiv

# Organize later
arxiv-organizer --directory ~/downloads/arxiv
```

### Combined Workflow
```bash
# Download + organize in one go
arxiv-organizer --download \
  --keywords "AI" \
  --period 7d \
  --max 10 \
  --smart-organize \
  --custom-topics "LLMs,Vision,Robotics" \
  --directory ~/research/current
```

## Troubleshooting

**Issue**: "No papers found to organize"
- **Check**: Are there PDFs with pattern `XXXX.XXXXX.pdf` in the directory?
- **Solution**: Verify the directory path and PDF filenames

**Issue**: Papers keep getting re-organized
- **Cause**: `library.json` was deleted or corrupted
- **Solution**: The index prevents re-processing; delete it only if you want to re-organize

**Issue**: Downloaded papers not being organized
- **Check**: Make sure you're using the same `--directory` for both download and organize
- **Solution**: Always use the same path, or omit for current directory
