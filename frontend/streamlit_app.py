"""
🌱 Sustainable Product Recommendation Agent — Streamlit Frontend

Premium white + green UI that communicates with the Flask backend.
"""

import os
import streamlit as st
import requests
from dotenv import load_dotenv

# Load environment
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:5000")

# ════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="🌱 Sustainable Product Agent",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ════════════════════════════════════════════════════════════════════════
# CUSTOM CSS — premium white + green identity
# ════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Import Google Font ──────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Root variables ──────────────────────────────────────────────── */
:root {
    --forest:      #1B5E20;
    --forest-dark: #0D3B11;
    --leaf:        #43A047;
    --leaf-light:  #66BB6A;
    --mint:        #E8F5E9;
    --mint-soft:   #F1F8E9;
    --white:       #FFFFFF;
    --text-dark:   #1A2E1A;
    --text-mid:    #3E5A3E;
    --text-light:  #6B8E6B;
    --border:      #C8E6C9;
    --shadow:      0 2px 12px rgba(27, 94, 32, 0.08);
    --shadow-hover:0 4px 20px rgba(27, 94, 32, 0.14);
    --radius:      12px;
}

/* ── Global resets ───────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}
.stApp {
    background: linear-gradient(180deg, var(--mint-soft) 0%, var(--white) 40%) !important;
}

/* Hide Streamlit menu & footer */
#MainMenu, footer, header {visibility: hidden;}

/* ── Hero section ────────────────────────────────────────────────── */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
    max-width: 800px;
    margin: 0 auto;
}
.hero-icon {
    font-size: 3rem;
    margin-bottom: 0.5rem;
}
.hero h1 {
    font-size: 2.4rem;
    font-weight: 800;
    color: var(--forest);
    margin: 0 0 0.6rem;
    letter-spacing: -0.5px;
}
.hero .tagline {
    font-size: 1.15rem;
    color: var(--text-mid);
    font-weight: 400;
    margin-bottom: 1.5rem;
}
.hero-pills {
    display: flex;
    justify-content: center;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin-bottom: 2rem;
}
.hero-pill {
    background: var(--mint);
    color: var(--forest);
    padding: 0.4rem 1rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
    border: 1px solid var(--border);
}

/* ── Search area ─────────────────────────────────────────────────── */
.search-helper {
    text-align: center;
    color: var(--text-light);
    font-size: 0.85rem;
    margin-top: -0.5rem;
    margin-bottom: 1rem;
}

/* Style the Streamlit text_area */
.stTextArea textarea {
    border: 2px solid var(--border) !important;
    border-radius: var(--radius) !important;
    font-size: 1rem !important;
    padding: 1rem !important;
    background: var(--white) !important;
    color: var(--text-dark) !important;
    transition: border-color 0.2s;
}
.stTextArea textarea:focus {
    border-color: var(--leaf) !important;
    box-shadow: 0 0 0 3px rgba(67, 160, 71, 0.15) !important;
}

/* ── Primary button ──────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, var(--forest) 0%, var(--leaf) 100%) !important;
    color: var(--white) !important;
    border: none !important;
    border-radius: var(--radius) !important;
    padding: 0.65rem 2.5rem !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px;
    transition: all 0.25s ease;
    box-shadow: 0 3px 10px rgba(27, 94, 32, 0.2);
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 5px 16px rgba(27, 94, 32, 0.3) !important;
}
.stButton > button:active {
    transform: translateY(0);
}

/* ── Section headers ─────────────────────────────────────────────── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 2.5rem 0 1.5rem;
    padding-bottom: 0.75rem;
    border-bottom: 2px solid var(--border);
}
.section-header h2 {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--forest);
    margin: 0;
}
.section-header .count-badge {
    background: var(--mint);
    color: var(--forest);
    padding: 0.2rem 0.7rem;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 600;
}

/* ── Product card ────────────────────────────────────────────────── */
.product-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    box-shadow: var(--shadow);
    transition: box-shadow 0.25s ease, transform 0.25s ease;
}
.product-card:hover {
    box-shadow: var(--shadow-hover);
    transform: translateY(-2px);
}
.product-name {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--forest-dark);
    margin: 0 0 0.3rem;
    line-height: 1.3;
}
.product-price {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--leaf);
    margin-bottom: 0.6rem;
}
.product-desc {
    color: var(--text-mid);
    font-size: 0.9rem;
    line-height: 1.55;
    margin-bottom: 1rem;
}
.feature-label, .sustain-label {
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.4rem;
}
.feature-label { color: var(--text-light); }
.sustain-label { color: var(--leaf); }

.feature-item {
    color: var(--text-mid);
    font-size: 0.88rem;
    padding: 0.15rem 0;
    line-height: 1.4;
}
.sustain-item {
    color: var(--forest);
    font-size: 0.88rem;
    padding: 0.15rem 0;
    line-height: 1.4;
}
.source-link {
    display: inline-block;
    margin-top: 0.8rem;
    color: var(--text-light);
    font-size: 0.82rem;
    text-decoration: none;
    transition: color 0.2s;
}
.source-link:hover { color: var(--forest); }

/* ── Explanation panel ───────────────────────────────────────────── */
.explain-panel {
    background: linear-gradient(135deg, var(--mint) 0%, var(--mint-soft) 100%);
    border: 1px solid var(--border);
    border-left: 4px solid var(--leaf);
    border-radius: var(--radius);
    padding: 1.4rem 1.6rem;
    margin-top: 1rem;
    color: var(--text-dark);
    font-size: 0.92rem;
    line-height: 1.65;
}
.explain-panel h4 {
    color: var(--forest);
    margin: 0 0 0.8rem;
    font-size: 1.05rem;
}

/* ── Status / info boxes ─────────────────────────────────────────── */
.info-box {
    background: var(--mint);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.2rem 1.5rem;
    text-align: center;
    color: var(--forest);
    font-size: 0.95rem;
    margin: 1rem 0;
}
.error-box {
    background: #FFF3E0;
    border: 1px solid #FFE0B2;
    border-left: 4px solid #FB8C00;
    border-radius: var(--radius);
    padding: 1rem 1.3rem;
    color: #E65100;
    font-size: 0.92rem;
    margin: 1rem 0;
}

/* ── Research details expander ───────────────────────────────────── */
.research-chip {
    display: inline-block;
    background: var(--mint);
    color: var(--forest);
    padding: 0.3rem 0.8rem;
    border-radius: 8px;
    font-size: 0.8rem;
    margin: 0.2rem 0.3rem 0.2rem 0;
    border: 1px solid var(--border);
}

/* ── Sidebar ─────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: var(--mint-soft) !important;
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--forest) !important;
}

/* ── Streamlit status widget ─────────────────────────────────────── */
.stStatusWidget { visibility: hidden; }

/* ── Responsive tweaks ───────────────────────────────────────────── */
@media (max-width: 768px) {
    .hero h1 { font-size: 1.7rem; }
    .hero .tagline { font-size: 1rem; }
    .product-card { padding: 1.1rem; }
}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ════════════════════════════════════════════════════════════════════════
if "products" not in st.session_state:
    st.session_state.products = []
if "user_query" not in st.session_state:
    st.session_state.user_query = ""
if "research_meta" not in st.session_state:
    st.session_state.research_meta = {}
if "explanations" not in st.session_state:
    st.session_state.explanations = {}  # keyed by product index
if "search_history" not in st.session_state:
    st.session_state.search_history = []


# ════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🌱 Sustainable Product Agent")
    st.markdown("*AI-powered product research*")
    st.markdown("---")
    st.markdown("### How It Works")
    st.markdown("""
1. **You describe** what you need  
2. **Grok** creates research queries  
3. **Tavily** searches the web  
4. **Products** are displayed  
5. **Ask Grok** why a product matches  
""")
    st.markdown("---")
    st.markdown("### Powered By")
    st.markdown("🤖 **Grok** — AI query planning & explanations")
    st.markdown("🔍 **Tavily** — Real-time web research")
    st.markdown("---")

    # Search history
    if st.session_state.search_history:
        st.markdown("### Recent Searches")
        for past_q in st.session_state.search_history[-5:]:
            st.markdown(f"- {past_q}")


# ════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ════════════════════════════════════════════════════════════════════════

def call_recommend(query: str) -> dict:
    """POST /api/recommend and return parsed JSON."""
    try:
        resp = requests.post(
            f"{BACKEND_URL}/api/recommend",
            json={"query": query},
            timeout=90,
        )
        return resp.json()
    except requests.exceptions.ConnectionError:
        return {"success": False, "data": None, "error": "Cannot connect to the backend. Is Flask running?"}
    except requests.exceptions.Timeout:
        return {"success": False, "data": None, "error": "The request timed out. Please try again."}
    except Exception as exc:
        return {"success": False, "data": None, "error": str(exc)}


def call_explain(user_query: str, product: dict) -> dict:
    """POST /api/explain and return parsed JSON."""
    try:
        resp = requests.post(
            f"{BACKEND_URL}/api/explain",
            json={"user_query": user_query, "product": product},
            timeout=60,
        )
        return resp.json()
    except requests.exceptions.ConnectionError:
        return {"success": False, "data": None, "error": "Cannot connect to the backend."}
    except requests.exceptions.Timeout:
        return {"success": False, "data": None, "error": "The explanation request timed out."}
    except Exception as exc:
        return {"success": False, "data": None, "error": str(exc)}


def render_product_card(product: dict, index: int):
    """Render a single product card with explanation support."""

    card_html = f"""
    <div class="product-card">
        <div class="product-name">{product.get('name', 'Unknown Product')}</div>
        <div class="product-price">{product.get('price', 'Price not available')}</div>
        <div class="product-desc">{product.get('description', 'No description available.')}</div>
    """

    # Features
    features = product.get("features", [])
    if features:
        card_html += '<div class="feature-label">Highlights</div>'
        for feat in features[:5]:
            card_html += f'<div class="feature-item">✓ {feat}</div>'

    # Sustainability info
    sustain = product.get("sustainability_info", [])
    if sustain:
        card_html += '<div class="sustain-label" style="margin-top:0.6rem;">Sustainability</div>'
        for s in sustain[:3]:
            card_html += f'<div class="sustain-item">🌱 {s}</div>'

    # Source
    source_url = product.get("source_url", "")
    source_title = product.get("source_title", "Source")
    if source_url:
        card_html += f'<a class="source-link" href="{source_url}" target="_blank" rel="noopener">📎 {source_title} ↗</a>'

    card_html += "</div>"
    st.markdown(card_html, unsafe_allow_html=True)

    # Action buttons
    col_why, col_clear = st.columns([1, 1])
    with col_why:
        if st.button("🤔 Why This Product?", key=f"why_{index}", use_container_width=True):
            with st.spinner("🧠 Analyzing why this product matches your request..."):
                result = call_explain(st.session_state.user_query, product)
                if result.get("success") and result.get("data"):
                    st.session_state.explanations[index] = result["data"]["explanation"]
                else:
                    st.session_state.explanations[index] = f"⚠ {result.get('error', 'Could not generate explanation.')}"
            st.rerun()

    # Show explanation if available
    if index in st.session_state.explanations:
        explanation_text = st.session_state.explanations[index]
        # Format the explanation nicely
        formatted = explanation_text.replace("\n", "<br>")
        st.markdown(f"""
        <div class="explain-panel">
            <h4>✨ Why This Product?</h4>
            {formatted}
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════
# HERO SECTION
# ════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="hero">
    <div class="hero-icon">🌱</div>
    <h1>Sustainable Product Recommendation Agent</h1>
    <div class="tagline">Discover products through AI-powered research</div>
    <div class="hero-pills">
        <span class="hero-pill">🤖 Search the web with AI</span>
        <span class="hero-pill">📦 Explore real products</span>
        <span class="hero-pill">💡 Understand why they match</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════
# SEARCH INPUT
# ════════════════════════════════════════════════════════════════════════

query = st.text_area(
    "What are you looking for?",
    placeholder="Example: I need sustainable headphones under ₹10,000 with long battery life",
    height=100,
    label_visibility="collapsed",
)

st.markdown(
    '<div class="search-helper">Describe what you need naturally. '
    'The AI will research relevant products for you.</div>',
    unsafe_allow_html=True,
)

col_search, col_clear_search = st.columns([3, 1])
with col_search:
    search_clicked = st.button("🔎 Find Products", use_container_width=True)
with col_clear_search:
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state.products = []
        st.session_state.user_query = ""
        st.session_state.research_meta = {}
        st.session_state.explanations = {}
        st.rerun()


# ════════════════════════════════════════════════════════════════════════
# SEARCH EXECUTION
# ════════════════════════════════════════════════════════════════════════

if search_clicked and query and query.strip():
    # Clear previous state
    st.session_state.products = []
    st.session_state.explanations = {}
    st.session_state.research_meta = {}
    st.session_state.user_query = query.strip()

    # Add to search history
    if query.strip() not in st.session_state.search_history:
        st.session_state.search_history.append(query.strip())

    with st.status("🌱 Researching products...", expanded=True) as status:
        st.write("🧠 Understanding your request...")
        st.write("🔍 Creating research queries...")
        st.write("🌐 Searching the web...")

        result = call_recommend(query.strip())

        if result.get("success") and result.get("data"):
            data = result["data"]
            st.session_state.products = data.get("products", [])
            st.session_state.research_meta = data.get("research", {})
            st.write("📦 Preparing product results...")
            status.update(
                label=f"✅ Found {len(st.session_state.products)} product(s)",
                state="complete",
                expanded=False,
            )
        else:
            error_msg = result.get("error", "Something went wrong.")
            status.update(label="⚠ Research incomplete", state="error", expanded=False)
            st.markdown(
                f'<div class="error-box">⚠ {error_msg}</div>',
                unsafe_allow_html=True,
            )

    st.rerun()

elif search_clicked and (not query or not query.strip()):
    st.markdown(
        '<div class="error-box">Please describe what you\'re looking for.</div>',
        unsafe_allow_html=True,
    )


# ════════════════════════════════════════════════════════════════════════
# RESULTS DISPLAY
# ════════════════════════════════════════════════════════════════════════

products = st.session_state.products
research = st.session_state.research_meta

if products:
    # Section header
    st.markdown(f"""
    <div class="section-header">
        <h2>Products Found</h2>
        <span class="count-badge">{len(products)} result{"s" if len(products) != 1 else ""}</span>
    </div>
    """, unsafe_allow_html=True)

    # Research details (collapsible)
    queries_used = research.get("queries_used", [])
    category = research.get("category", "")
    if queries_used:
        with st.expander("🔬 Research Details"):
            if category:
                st.markdown(f"**Category detected:** {category}")
            st.markdown("**Search queries used:**")
            chips_html = "".join(
                f'<span class="research-chip">{q}</span>' for q in queries_used
            )
            st.markdown(chips_html, unsafe_allow_html=True)

    # Product cards in responsive columns
    col_left, col_right = st.columns(2)
    for i, product in enumerate(products):
        with (col_left if i % 2 == 0 else col_right):
            render_product_card(product, i)

elif st.session_state.user_query and not products:
    st.markdown("""
    <div class="info-box">
        🔍 No relevant products were found.<br>
        Try adding a product category, budget, or specific requirement.
    </div>
    """, unsafe_allow_html=True)
