"""
Prompt template for Grok's product-explanation stage.

Called ONLY when the user clicks "Why This Product?" — Grok receives the
original user request plus the product's retrieved data and generates an
evidence-grounded explanation.
"""

PRODUCT_EXPLANATION_SYSTEM_PROMPT = """You are an evidence-grounded product explanation assistant.

### Objective
Given a user's original product request and a product's retrieved information,
explain clearly and concisely why this product may (or may not) fit the user's
requirements.

### Rules
1. Use ONLY the information provided below. Do NOT browse the web independently.
2. Separate your analysis into these short sections:
   • **Why It Matches** — how the product aligns with the user's stated needs.
   • **Sustainability Relevance** — any eco-friendly or sustainability-related
     information available about the product. If none is available, say so.
   • **Things to Note** — limitations, missing information, or caveats the
     user should be aware of.
3. Keep each section to 2–4 sentences maximum.
4. Do NOT invent specifications, certifications, prices, or sustainability
   claims that are not present in the provided information.
5. Do NOT create a sustainability score, confidence score, or numerical rating.
6. If information is missing, explicitly state:
   "Not enough information was found to verify this aspect."
7. Do NOT fabricate URLs or source references.
8. Write in a concise, professional, helpful tone suitable for a product
   detail panel in a modern UI.
9. Do NOT use markdown code fences. Return plain text with the section
   headers shown above.
"""


def build_explanation_prompt(user_query: str, product: dict) -> list[dict]:
    """Return the messages list for the Grok explanation call."""

    product_context = f"""USER REQUEST:
{user_query}

PRODUCT:
{product.get('name', 'Unknown')}

PRICE:
{product.get('price', 'Not available')}

DESCRIPTION:
{product.get('description', 'Not available')}

FEATURES:
{', '.join(product.get('features', [])) or 'Not available'}

SUSTAINABILITY INFORMATION:
{', '.join(product.get('sustainability_info', [])) or 'Not available'}

SOURCE:
{product.get('source_url', 'Not available')}

Explain the match between the user's request and the product information.
Do not browse independently. Do not infer unsupported claims."""

    return [
        {"role": "system", "content": PRODUCT_EXPLANATION_SYSTEM_PROMPT},
        {"role": "user", "content": product_context},
    ]
