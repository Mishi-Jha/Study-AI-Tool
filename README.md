# CS Study Buddy — AI Agent with RAG

An intelligent AI tutor that combines web search with your personal study notes to answer questions and generate MCQs. Built with agentic AI, retrieval-augmented generation (RAG), and real-time tool calling.

## Features

- **Agentic AI** — The model decides whether to search the web, your notes, or both
- **RAG Pipeline** — Upload PDFs; AI retrieves relevant sections and answers based on your material
- **MCQ Generation** — Automatically generates practice questions from your study notes
- **Web Search** — Real-time answers via Tavily Search API for recent topics
- **Markdown Rendering** — Clean, formatted responses with bold, code blocks, and lists
- **Conversation Memory** — Maintains context across multiple turns

## How It Works

1. **Upload a PDF** — Your study notes get split into chunks and converted to embeddings
2. **Ask a Question** — The agent analyzes your query
3. **Tool Calling** — Agent decides: search web OR search notes OR both
4. **Retrieval** — Most relevant chunks are pulled from your PDF
5. **Generation** — AI synthesizes an answer with explanations and MCQs

## Tech Stack

**Backend:**
- Flask (REST API)
- LangChain (orchestration)
- Groq Llama 3.1 8B (LLM)
- ChromaDB (vector database)
- Tavily Search (web search)
- HuggingFace Embeddings

**Frontend:**
- Vanilla JavaScript
- HTML/CSS
- marked.js (markdown rendering)

## Quick Start

### Prerequisites
- Python 3.9+
- Groq API key ([console.groq.com](https://console.groq.com))
- Tavily API key ([tavily.com](https://tavily.com))

### Setup

```bash
# Clone the repo
git clone https://github.com/Mishi-Jha/cs-study-buddy.git
cd cs-study-buddy

# Install dependencies
cd backend
pip install -r requirements.txt

# Create .env file
echo "GROQ_API_KEY=your_key_here" > .env
echo "TAVILY_API_KEY=your_key_here" >> .env

# Run backend
python app.py
```

### Start Frontend
- Open `frontend/index.html` with Live Server in VS Code
- Or open at `http://127.0.0.1:5500`

## Usage

1. **Upload Notes** — Click "Upload Notes", select a PDF
2. **Ask Questions** — Type any question about your material or general CS topics
3. **Get MCQs** — Request "generate 10 MCQs from first 5 pages"
4. **Get Explanations** — AI explains complex topics with examples

## Architecture
User Question
↓
Agent (LangChain + Groq)
↓
Tool Decision
├─→ search_notes (ChromaDB)
├─→ tavily_search (Web)
└─→ both
↓
Retrieve Relevant Content
↓
Generate Answer + Format
↓
Return to User


## What I Learned Building This

- **Phase 1** — LLM APIs, prompt engineering, conversation memory
- **Phase 2** — RAG: embeddings, vector databases, semantic search
- **Phase 3** — LangChain abstractions, document loaders, text splitters
- **Phase 4** — AI agents, tool calling, agentic decision-making

## Future Improvements

- Deploy to cloud (Render backend, Vercel frontend)
- Add RAG evaluation harness to measure retrieval quality
- Support multiple file formats (Word, images, PowerPoint)
- Multi-user accounts with persistent notes
- Citation tracking (show which notes answered each question)

## License

MIT

## Author

[Mishi Jha](https://github.com/Mishi-Jha)