import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="Catholic Sacramentals", layout="wide")

BASE = Path(__file__).parent
DATA_FILE = BASE / "data" / "sacramentals.json"
LANG_DIR = BASE / "data" / "lang"
ASSETS = BASE / "assets"
ICONS = ASSETS / "icons"
PLACEHOLDER = ASSETS / "placeholder.png"
SUPPORTED_LANGS = ["en","fr"]

@st.cache_data
def load_items():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_lang(code: str):
    file = LANG_DIR / f"{code}.json"
    if not file.exists():
        file = LANG_DIR / "en.json"
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)

def pick_lang_from_browser():
    try:
        from streamlit_javascript import st_javascript
        nav_lang = st_javascript("return (navigator.language || navigator.userLanguage || 'en');")
        if isinstance(nav_lang, str):
            code = nav_lang.split('-')[0].lower()
            return code if code in SUPPORTED_LANGS else 'en'
    except Exception:
        pass
    return 'en'

def detect_lang():
    qlang = st.query_params.get("lang", [None])[0]
    if qlang and qlang in SUPPORTED_LANGS:
        return qlang
    if 'lang' in st.session_state and st.session_state['lang'] in SUPPORTED_LANGS:
        return st.session_state['lang']
    return pick_lang_from_browser()

def set_lang(lang_code: str):
    st.session_state['lang'] = lang_code
    st.query_params['lang'] = lang_code

def category_bar(display_categories, current, lang_code):
    st.markdown("""
        <style>
        .cat-bar { display:flex; gap:12px; overflow-x:auto; padding:8px 0 2px 0; }
        .cat-pill {
            text-align:center; min-width:92px; padding:8px 12px;
            border-radius:14px; border:1px solid rgba(0,0,0,.08);
            background: rgba(255,255,255,.7);
            box-shadow: 0 1px 2px rgba(0,0,0,.04);
            text-decoration:none; color:inherit; display:inline-flex;
            flex-direction:column; align-items:center; justify-content:center;
            transition: transform .08s ease, box-shadow .12s ease;
        }
        .cat-pill:hover { transform: translateY(-1px); box-shadow: 0 4px 10px rgba(0,0,0,.08); }
        .cat-pill.selected { border-color: rgba(60,60,220,.25); box-shadow:0 2px 8px rgba(60,60,220,.15); background: rgba(60,60,220,.06); }
        .cat-pill img { width:42px; height:42px; object-fit:contain; margin-bottom:6px; }
        .cat-pill span { font-size:12px; white-space:nowrap; }
        .card { border:1px solid rgba(0,0,0,.08); border-radius:16px; padding:12px; background:white; box-shadow:0 1px 3px rgba(0,0,0,.06); transition: box-shadow .12s ease, transform .08s ease; }
        .card:hover { box-shadow:0 6px 16px rgba(0,0,0,.10); transform: translateY(-1px); }
        </style>
    """, unsafe_allow_html=True)

    pills = ["<div class='cat-bar'>"]
    for c in display_categories:
        key = c.lower()
        icon = ICONS / f"{key}.png"
        selected = " selected" if c == current else ""
        href = f"?cat={c}&lang={lang_code}"
        img_src = str(icon).replace(str(BASE) + "/", "")
        pills.append(f"<a class='cat-pill{selected}' href='{href}'><img src='{img_src}' alt='{c}'/><span>{c}</span></a>")
    pills.append("</div>")
    st.markdown("\n".join(pills), unsafe_allow_html=True)

def main():
    lang_code = detect_lang()
    lang = load_lang(lang_code)

    with st.sidebar:
        st.markdown(f"### {lang['language_label']}")
        chosen = st.selectbox("", SUPPORTED_LANGS, index=SUPPORTED_LANGS.index(lang_code))
        if chosen != lang_code:
            set_lang(chosen)
            st.rerun()

    st.title(lang["title"]) 
    st.write(lang["subtitle"]) 

    items = load_items()
    # Categories are fixed English names for now (match icons)
    categories = ["All"] + sorted({it["category"] for it in items})
    current_cat = st.query_params.get("cat", ["All"])[0]
    if current_cat not in categories:
        current_cat = "All"

    category_bar(categories, current_cat, lang_code)

    q = st.text_input(lang["search_placeholder"], "").strip().lower()

    def match(it):
        in_cat = (current_cat == "All") or (it["category"] == current_cat)
        if not q:
            return in_cat
        return in_cat and (q in it["name"].lower() or q in it["description"].lower())

    filtered = [it for it in items if match(it)]
    st.caption(lang["showing"].format(shown=len(filtered), total=len(items)))

    if not filtered:
        st.info(lang["no_results"]) 
        return

    cols = st.columns(3)
    for i, it in enumerate(filtered):
        with cols[i % 3]:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            img_path = ASSETS / it.get("image", "")
            if not img_path.exists():
                img_path = PLACEHOLDER
            st.image(str(img_path), use_container_width=True)
            st.subheader(it["name"]) 
            st.caption(it["category"]) 
            st.write(it["description"]) 
            st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
