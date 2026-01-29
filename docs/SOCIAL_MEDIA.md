# Social Media Announcements

## Twitter/X Post (Multiple Tweet Thread)

### Tweet 1 (Main)
```
🚀 Introducing arxiv-organizer v2.0 - Your AI-Powered Research Assistant!

Automatically download, organize, and enrich arXiv papers using Google's Gemini AI.

✨ Smart Downloads
🤖 AI Classification
📚 Rich Metadata
⚡ Lightning Fast

pip install arxiv-organizer

Thread 👇
```

### Tweet 2
```
Why v2.0 is a game-changer:

🔍 Smart Judge: Filter papers by natural language
"Papers about LLM reasoning, exclude surveys"

📂 Custom Topics: Organize by YOUR research areas
Not just arXiv categories → "Agents", "RAG", "Multimodal"

🏷️ AI Enrichment: Auto-generated summaries & tags
```

### Tweet 3
```
Example workflow:

arxiv-organizer --download \
  --keywords "LLM reasoning" \
  --period 7d \
  --smart-judge \
  --judge-criteria "Novel reasoning methods" \
  --smart-organize \
  --custom-topics "CoT,ReAct,Planning"

One command. Fully organized library. 🎯
```

### Tweet 4
```
🔓 Completely open source & optional AI

Works perfectly WITHOUT any API keys
Just uses arXiv categories (still super useful!)

Want AI superpowers?
→ Free Gemini API
→ Add .env file
→ Done

Docs: github.com/mozayed007/arxiv-organizer

#MachineLearning #AI #ResearchTools
```

---

## LinkedIn Post

### Version 1 (Professional)
```
Excited to share arxiv-organizer v2.0! 🚀

After months of development, I've released a major update to my open-source research paper management tool. It now leverages Google's Gemini AI to intelligently organize your academic library.

What's New in v2.0:

📥 Smart Downloads
   → Query arXiv by keywords, topics, or natural language
   → Filter by time period (last day to 30 years)
   → Batch download with progress tracking

🤖 AI-Powered Organization
   → Classify papers into YOUR custom research topics
   → Auto-generate summaries and tags
   → Works offline - AI is completely optional!

⚡ Performance & Features
   → Parallel processing for speed
   → Rich JSON metadata for every paper
   → Smart updates (skip already processed papers)
   → Pydantic-based type safety

Real Example:
Instead of manually sorting 100 papers into arXiv's generic categories, I now sort them into "Agents", "RAG", "Multimodal" - topics that matter to MY research.

The best part? It's backward compatible and FREE. No breaking changes from v1.x.

Installation:
pip install arxiv-organizer

GitHub: github.com/mozayed007/arxiv-organizer

Would love to hear your feedback! What features would help YOUR research workflow?

#OpenSource #MachineLearning #ResearchTools #Python #AI #AcademicResearch
```

### Version 2 (Story-Driven)
```
Ever spent hours organizing downloaded papers? 📚

I did. Every week. Until I automated it.

Today, I'm releasing arxiv-organizer v2.0 - and it's powered by AI.

The Problem:
   • Download 50 papers on "LLMs"
   • Half are about benchmarks (don't want)
   • Half need sorting into specific topics
   • 2 hours wasted on manual organization

The Solution:
   One command. AI does the heavy lifting.

arxiv-organizer --download \
  --keywords "large language models" \
  --smart-judge \
  --judge-criteria "Novel architectures, exclude benchmarks" \
  --smart-organize \
  --custom-topics "Transformers,Attention,FineTuning"

Result:
   ✅ Downloads only relevant papers
   ✅ Sorts into MY research topics
   ✅ Generates summaries & tags
   ✅ Creates searchable JSON metadata
   
   Time saved: ~2 hours/week

Key Features:
   → Natural language filtering ("Papers about X, excluding Y")
   → Custom topic classification (not just arXiv categories)
   → Zero setup if you don't want AI (works great without it)
   → 100% open source

Built with: Python, Pydantic, Google Gemini API

Try it: pip install arxiv-organizer
Docs: github.com/mozayed007/arxiv-organizer

What repetitive tasks in YOUR workflow could be automated? Let's discuss! 👇

#ProductivityTools #AI #ResearchAutomation #OpenSource #Python
```

---

## Reddit Posts

### r/MachineLearning
**Title:** [P] arxiv-organizer v2.0 - AI-powered paper organization with Gemini

**Body:**
```
I've been working on a tool to automate my paper organization workflow, and today I'm releasing v2.0 with some major AI features.

**What it does:**
- Downloads papers from arXiv based on queries
- Filters using natural language (e.g., "Papers about reasoning, exclude surveys")
- Classifies into custom topics using Gemini
- Auto-generates summaries and tags
- Creates a searchable library with rich metadata

**Example:**
```bash
arxiv-organizer --download \
  --keywords "reinforcement learning" \
  --period 30d \
  --smart-judge \
  --judge-criteria "Novel algorithms for continuous control" \
  --smart-organize \
  --custom-topics "ModelFree,ModelBased,OfflineRL"
```

**Key points:**
- All AI features are optional (works great without them)
- Uses free Gemini API
- Pydantic for type safety
- Parallel processing
- MIT licensed

GitHub: https://github.com/mozayed007/arxiv-organizer
PyPI: pip install arxiv-organizer

Happy to answer questions!
```

### r/Python
**Title:** [Project] arxiv-organizer - Automate your research paper library with Python & AI

**Body:**
```
Built a tool to solve a personal problem: organizing hundreds of arXiv papers.

**Tech Stack:**
- Pydantic for data validation
- ThreadPoolExecutor for parallel processing
- Google Generative AI (Gemini)
- tqdm for progress bars
- arXiv API

**Architecture highlights:**
- Clean separation: downloader, organizer, AI client
- Graceful degradation (runs without API keys)
- Type-safe with Pydantic models
- Config via .env files (pydantic-settings)

**What I learned:**
- Pydantic makes config management so much cleaner
- Graceful degradation is worth the extra checks
- Users love optional features over forced dependencies

Check it out: https://github.com/mozayed007/arxiv-organizer

Open to feedback and PRs!
```

---

## Email to Research Communities

**Subject:** Introducing arxiv-organizer v2.0 - AI-Powered Paper Management

**Body:**
```
Hi [Community],

I wanted to share a tool I've been building that might help with managing research papers.

arxiv-organizer v2.0 is an open-source Python package that:
- Auto-downloads papers from arXiv
- Organizes them by your custom research topics (using AI)
- Generates searchable metadata

It's designed to save time on the repetitive task of paper organization.

Installation: pip install arxiv-organizer
Documentation: https://github.com/mozayed007/arxiv-organizer

All features work without AI, but you can opt-in to use Gemini for smarter classification.

Would love to hear your thoughts!

Best,
MoZayed
```
