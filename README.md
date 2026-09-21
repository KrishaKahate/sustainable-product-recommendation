# 🌱 Sustainable Product Recommendation Agent

An AI-powered product research and recommendation interface that uses **Grok** for intelligent query generation and **Tavily** for real-time web research.

---

## Problem Statement

Finding sustainable, eco-friendly products is time-consuming. Users must manually search across multiple websites, compare specifications, and verify sustainability claims. This application automates that research using AI.

## Architecture

```
User → Streamlit → Flask → Grok (query planning) → Tavily (web search) → Flask → Streamlit
                                                                                      │
                          User clicks "Why This Product?" → Flask → Grok (explanation) ↵
```

**Grok** has exactly two responsibilities:
1. Analyze the user's request and generate optimized research queries
2. Explain why a selected product matches the user's requirements

**Tavily** has exactly one responsibility:
- Perform real-time web research using Grok's queries

## Features

- 🤖 **AI Query Planning** — Grok analyzes natural-language requests and generates targeted search queries
- 🔍 **Real-Time Web Research** — Tavily searches the current web for actual products
- 📦 **Clean Product Display** — Results displayed as modern, readable product cards
- 💡 **Explainable AI** — "Why This Product?" generates evidence-grounded explanations
- 🌱 **Sustainability Focus** — Queries and parsing prioritize eco-friendly information
- ♻️ **No Hallucination** — The system never invents products, prices, or certifications

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Backend | Flask, Flask-CORS |
| AI | Grok (xAI API) |
| Web Search | Tavily API |
| HTTP | requests |
| Config | python-dotenv |

## Project Structure

```
sustainable-product-agent/
│
├── frontend/
│   └── streamlit_app.py          # Streamlit UI
│
├── backend/
│   ├── app.py                     # Flask entry point
│   ├── config.py                  # Environment & configuration
│   │
│   ├── routes/
│   │   ├── recommend.py           # POST /api/recommend
│   │   └── explain.py             # POST /api/explain
│   │
│   ├── services/
│   │   ├── grok_service.py        # xAI API client
│   │   ├── tavily_service.py      # Tavily search client
│   │   └── product_parser.py      # Result → product transformer
│   │
│   └── prompts/
│       ├── query_generation.py    # Grok query-planning prompt
│       └── product_explanation.py # Grok explanation prompt
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

### 1. Clone and install dependencies

```bash
cd sustainable-product-agent
pip install -r requirements.txt
```

### 2. Configure API keys

Copy the example environment file and add your keys:

```bash
cp .env.example .env
```

Edit `.env`:

```env
XAI_API_KEY=your_xai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
GROK_MODEL=grok-3-mini
BACKEND_URL=http://127.0.0.1:5000
```

- **XAI_API_KEY**: Get from [x.ai](https://console.x.ai/)
- **TAVILY_API_KEY**: Get from [tavily.com](https://app.tavily.com/)
- **GROK_MODEL**: Optional — defaults to `grok-3-mini` if left blank

### 3. Run the backend

```bash
python backend/app.py
```

Flask starts on `http://127.0.0.1:5000`. Verify with:

```bash
curl http://127.0.0.1:5000/api/health
```

### 4. Run the frontend

In a separate terminal:

```bash
streamlit run frontend/streamlit_app.py
```

Opens on `http://localhost:8501`.

## Usage

### Example Query

> "I want sustainable headphones under ₹10,000 with good battery life"

### What Happens

1. Streamlit sends the query to Flask (`POST /api/recommend`)
2. Flask calls Grok, which analyzes the request and generates 3–5 search queries
3. Flask sends those queries to Tavily for web research
4. Tavily results are parsed into clean product objects
5. Streamlit displays product cards with name, price, features, and sustainability info
6. User clicks **"Why This Product?"** on any card
7. Flask sends the product + original query to Grok (`POST /api/explain`)
8. Grok generates an evidence-grounded explanation displayed in the UI

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/recommend` | Product research |
| POST | `/api/explain` | Product explanation |

### POST /api/recommend

```json
{
  "query": "sustainable headphones under ₹10,000"
}
```

### POST /api/explain

```json
{
  "user_query": "sustainable headphones under ₹10,000",
  "product": {
    "name": "Product Name",
    "price": "₹8,499",
    "description": "...",
    "features": [],
    "sustainability_info": [],
    "source_url": "https://..."
  }
}
```

## Limitations

- Product parsing is heuristic-based — web pages vary, so some fields may show "Not available"
- No persistent storage — results are per-session only
- No user authentication
- Depends on Tavily and xAI API availability
- Results reflect what's currently on the web, not a curated database

## Future Enhancements

- Add product image extraction from web results
- Support multiple languages and regions
- Add product comparison feature
- Implement session-based search history persistence
- Add export to CSV/PDF
- Support voice input for product queries

---

*Built as a lightweight AI prototype demonstrating LLM prompt engineering, web research orchestration, and explainable AI interaction.*
