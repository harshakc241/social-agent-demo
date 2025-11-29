# app.py (improved UI)
import os
import json
import streamlit as st
from datetime import datetime
from io import StringIO

# Optional: OpenAI import
try:
    import openai
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False

# ==============
# Configuration
# ==============
DEFAULT_MODEL = "gpt-3.5-turbo"
MODELS = [DEFAULT_MODEL, "gpt-4o-mini", "gpt-4", "offline"]

PROMPT_JSON_STRICT = """You are a JSON-producing social media writer.
Return ONLY a strict JSON array of objects, no extra text or commentary.
Each object must have: idea (one-line), caption (string), hashtags (array of strings).
Topic: {topic}
Platform: {platform}
Tone: {tone}
Count: {count}
"""

PROMPT_RELAXED = """You are a creative social media content writer.
Given a topic, platform, tone and requested number of posts, produce for each post:
1) A short content idea (one line).
2) A caption (max 220 words).
3) 5 relevant hashtags.
Keep captions platform-appropriate (Instagram: engaging + emojis; X: concise; LinkedIn: professional).
Output as a JSON array with fields: idea, caption, hashtags.
Topic: {topic}
Platform: {platform}
Tone: {tone}
Count: {count}
"""

FALLBACK_LIBRARY = {
    "sustainable fashion": [
        {
            "idea": "Upcycle denim into an everyday bag",
            "caption": "Turn old jeans into a new favorite — DIY upcycled denim bag in 3 easy steps 🧵♻️. Reduce waste, look great, and save money. Tap for the mini guide!",
            "hashtags": ["#sustainablefashion", "#upcycle", "#ecofriendly", "#diyfashion", "#slowfashion"]
        },
        {
            "idea": "Capsule wardrobe staples",
            "caption": "Less is more. Build a capsule wardrobe with 10 timeless pieces that mix & match for every season. Save space, time, and the planet 🌍✨.",
            "hashtags": ["#capsulewardrobe", "#sustainablefashion", "#minimalism", "#ethicalstyle", "#consciousliving"]
        }
    ],
    "product launch": [
        {
            "idea": "Sneak-peek demo video",
            "caption": "We’re launching something new — here’s a 15s sneak peek! Sign up for early access. 🚀",
            "hashtags": ["#productlaunch", "#startup", "#comingsoon", "#innovation", "#signup"]
        }
    ]
}

# ===========
# Helpers
# ===========
def call_openai_chat(model, prompt, temperature=0.8, max_tokens=800):
    if model == "offline":
        raise RuntimeError("offline model selected")
    if not OPENAI_AVAILABLE:
        raise RuntimeError("openai package not available")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set in environment")
    openai.api_key = api_key
    resp = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return resp["choices"][0]["message"]["content"]

def parse_json_output(maybe_json_text):
    try:
        return json.loads(maybe_json_text)
    except Exception:
        start = maybe_json_text.find('[')
        end = maybe_json_text.rfind(']')
        if start != -1 and end != -1 and end > start:
            try:
                snippet = maybe_json_text[start:end+1]
                return json.loads(snippet)
            except Exception:
                return None
        return None

def fallback_generate(topic, count):
    lib = FALLBACK_LIBRARY.get(topic.lower())
    if lib:
        return lib[:count]
    out = []
    for i in range(count):
        out.append({
            "idea": f"{topic} idea #{i+1}",
            "caption": f"Sample caption for {topic} — short, catchy, ready to post.",
            "hashtags": [f"#{topic.replace(' ', '')}", "#trending", "#mustread", "#tips", "#daily"]
        })
    return out

def dataframe_from_results(results):
    rows = []
    for i, item in enumerate(results, start=1):
        idea = item.get("idea") if isinstance(item, dict) else str(item)
        caption = item.get("caption") if isinstance(item, dict) else ""
        hashtags = " ".join(item.get("hashtags", [])) if isinstance(item, dict) else ""
        rows.append({"post_no": i, "idea": idea, "caption": caption, "hashtags": hashtags})
    return rows

# ===========
# Styling
# ===========
st.set_page_config(page_title="Social Media Agent — Improved UI", layout="wide")
# small CSS to make it look nicer
st.markdown(
    """
    <style>
    .app-header {display:flex; align-items:center; gap:12px;}
    .title {font-size:30px; font-weight:700; margin-bottom:0px;}
    .subtitle {color: #6b7280; margin-top:4px; margin-bottom:8px;}
    .card {border-radius:10px; padding:14px; background: #ffffff; box-shadow: 0 1px 6px rgba(0,0,0,0.06); margin-bottom:12px;}
    .small-muted {color:#6b7280; font-size:13px;}
    .hashtag {background:#f3f4f6; padding:6px 8px; border-radius:999px; margin-right:6px; display:inline-block; font-size:13px;}
    </style>
    """,
    unsafe_allow_html=True
)

# ===========
# Sidebar (settings)
# ===========
with st.sidebar:
    st.header("Settings")
    model = st.selectbox("Model", MODELS, index=0)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.8, 0.05)
    strict_json = st.checkbox("Force strict JSON output (recommended)", value=True)
    st.write("---")
    st.write("API status:")
    if model == "offline":
        st.success("Offline mode selected (no API calls)")
    else:
        if not OPENAI_AVAILABLE:
            st.warning("openai package missing — install `openai` to use live API")
        elif os.getenv("OPENAI_API_KEY") is None:
            st.warning("OPENAI_API_KEY not set in environment")
        else:
            st.success("OpenAI API key found")
    st.write("---")
    st.markdown("**Presets**")
    if st.button("Sustainable fashion"):
        st.session_state['topic'] = "sustainable fashion"
    if st.button("Product launch"):
        st.session_state['topic'] = "product launch"
    if st.button("Mental health tips"):
        st.session_state['topic'] = "mental health tips"
    st.write("---")
    if st.button("Clear outputs"):
        st.session_state['results'] = None

# ===========
# Page header + inputs
# ===========
col1, col2 = st.columns([3,2])
with col1:
    st.markdown('<div class="app-header"><div><h1 class="title">Social Media Agent</h1><div class="subtitle">Generate post ideas, captions & hashtags — fast demo</div></div></div>', unsafe_allow_html=True)
with col2:
    st.write("")  # placeholder for future buttons (e.g., help)

st.markdown("A compact UI to prototype social media captions. Use the `offline` model when you don't have an API key.")

# Input form
with st.form("main_form", clear_on_submit=False):
    topic = st.text_input("Topic / Product / Theme", value=st.session_state.get('topic', "sustainable fashion"), key="topic")
    platform = st.selectbox("Platform", ["Instagram", "Twitter/X", "LinkedIn", "Facebook", "TikTok"], index=0)
    tone = st.selectbox("Tone", ["Friendly", "Professional", "Witty", "Inspirational", "Informative"], index=0)
    count = st.slider("Number of posts", 1, 5, 3, key="count")
    submitted = st.form_submit_button("Generate")

# ===========
# Generate / Call logic
# ===========
if submitted:
    st.session_state['results'] = None
    status_area = st.empty()
    try:
        if model == "offline" or not OPENAI_AVAILABLE or os.getenv("OPENAI_API_KEY") is None:
            status_area.info("Using offline fallback (deterministic demo)")
            results = fallback_generate(topic, count)
        else:
            prompt = PROMPT_JSON_STRICT.format(topic=topic, platform=platform, tone=tone, count=count) if strict_json else PROMPT_RELAXED.format(topic=topic, platform=platform, tone=tone, count=count)
            status_area.info("Calling OpenAI...")
            raw = call_openai_chat(model, prompt, temperature=temperature)
            parsed = parse_json_output(raw)
            if parsed is None:
                status_area.warning("Model output could not be parsed as strict JSON — showing raw output and using heuristic fallback.")
                st.code(raw)
                blocks = [b for b in raw.split("\n\n") if b.strip()]
                results = []
                for b in blocks[:count]:
                    results.append({"idea": b.splitlines()[0][:80], "caption": b, "hashtags": []})
            else:
                results = parsed
        st.session_state['results'] = results
        status_area.success("Done — results ready.")
    except Exception as e:
        status_area.error(f"Error: {e}")
        results = fallback_generate(topic, count)
        st.session_state['results'] = results

# ===========
# Results area
# ===========
results = st.session_state.get('results')
if results:
    st.write("### Generated posts")
    # show copy/preset/download area at top
    rows = dataframe_from_results(results)
    # Create CSV and JSON for download
    import pandas as pd
    df = pd.DataFrame(rows)
    csv_data = df.to_csv(index=False)
    json_data = json.dumps(results, indent=2, ensure_ascii=False)
    col_dl1, col_dl2, col_dl3 = st.columns([1,1,4])
    with col_dl1:
        st.download_button("Download CSV", csv_data, file_name=f"content_{topic.replace(' ','_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", mime="text/csv")
    with col_dl2:
        st.download_button("Download JSON", json_data, file_name=f"content_{topic.replace(' ','_')}.json", mime="application/json")
    with col_dl3:
        st.markdown('<div class="small-muted">Tip: Use the copy buttons on each caption card to quickly copy into your social scheduler.</div>', unsafe_allow_html=True)

    # layout results as cards
    left_col, right_col = st.columns([1,1])
    # iterate results and place them as card blocks two per row
    for i, item in enumerate(results):
        card_html = f"""
        <div class="card">
            <strong>Post {i+1}: {item.get('idea','')}</strong><br><br>
            <div style="white-space:pre-wrap;">{item.get('caption','')}</div><br>
        """
        hashtags_html = " ".join([f"<span class='hashtag'>{h}</span>" for h in item.get('hashtags',[])])
        card_html += f"<div>{hashtags_html}</div>"
        card_html += "</div>"
        # choose column
        target_col = left_col if i % 2 == 0 else right_col
        with target_col:
            st.markdown(card_html, unsafe_allow_html=True)
            # a text area to select and copy caption if user prefers
            caption_id = f"caption_{i}"
            st.text_area("Caption (editable)", value=item.get('caption',''), key=caption_id, height=120)
            # copy button (JS)
            copy_js = f"""
            <script>
            function copyToClipboard{i}() {{
                const text = document.querySelectorAll('textarea')[{i}].value;
                navigator.clipboard.writeText(text).then(()=>{{alert('Caption copied to clipboard');}});
            }}
            </script>
            <button onclick="copyToClipboard{i}()">Copy caption</button>
            """
            # Use components.html to inject button & script (works in Streamlit)
            st.components.v1.html(copy_js, height=40)
            st.write("---")

    # show raw JSON collapsible
    with st.expander("Raw JSON output"):
        st.code(json_data)
else:
    st.info("No generated results yet — enter topic and click Generate.")

# ===========
# Footer notes
# ===========
st.markdown("---")
st.markdown("Built for fast prototyping. Improvements: add rich image previews, scheduling integration, multi-user workspace.")
