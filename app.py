
import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title='Catholic Sacramentals', layout='wide')

BASE = Path(__file__).parent
DATA_FILE = BASE / 'data' / 'sacramentals.json'
LANG_DIR = BASE / 'data' / 'lang'
ASSETS = BASE / 'assets' / 'images'
ICONS = BASE / 'assets' / 'icons'
PLACEHOLDER = ASSETS / 'placeholder.jpg'

SUPPORTED = ['en','fr','es','it','tl']

@st.cache_data
def load_items():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

@st.cache_data
def load_lang(code):
    p = LANG_DIR / f'{code}.json'
    if not p.exists():
        p = LANG_DIR / 'en.json'
    with open(p, 'r', encoding='utf-8') as f:
        return json.load(f)

def browser_lang():
    try:
        from streamlit_javascript import st_javascript
        nav = st_javascript("return (navigator.language || navigator.userLanguage || 'en');")
        if isinstance(nav, str):
            return nav.split('-')[0].lower()
    except Exception:
        pass
    return 'en'

def detect_lang():
    q = st.query_params.get('lang', [None])[0]
    if q and q in SUPPORTED:
        return q
    if 'lang' in st.session_state and st.session_state['lang'] in SUPPORTED:
        return st.session_state['lang']
    bl = browser_lang()
    return bl if bl in SUPPORTED else 'en'

def set_lang(c):
    st.session_state['lang'] = c
    st.query_params['lang'] = c

def category_bar(cats, current, lang_code):
    st.markdown(\"\"\"
        <style>
        .cat-bar { display:flex; gap:12px; overflow-x:auto; padding:8px 0 2px 0; }
        .cat-pill { text-align:center; min-width:92px; padding:8px 12px; border-radius:14px; border:1px solid rgba(0,0,0,.08); background: rgba(255,255,255,.7); box-shadow:0 1px 2px rgba(0,0,0,.04); text-decoration:none; color:inherit; display:inline-flex; flex-direction:column; align-items:center; justify-content:center; }
        .cat-pill.selected { border-color: rgba(60,60,220,.25); box-shadow:0 2px 8px rgba(60,60,220,.15); background: rgba(60,60,220,.06); }
        .cat-pill img { width:42px; height:42px; object-fit:contain; margin-bottom:6px; }
        .cat-pill span { font-size:12px; white-space:nowrap; }
        </style>
    \"\"\", unsafe_allow_html=True)
    pills = ['<div class=\"cat-bar\">']
    for cat in cats:
        key = cat.lower()
        icon = ICONS / f\"{key}.jpg\"
        selected = ' selected' if cat == current else ''
        href = f'?cat={cat}&lang={lang_code}'
        img_src = str(icon).replace(str(BASE) + '/', '')
        pills.append(f\"<a class='cat-pill{selected}' href='{href}'><img src='{img_src}' alt='{cat}'/><span>{cat}</span></a>\")
    pills.append('</div>')
    st.markdown('\\n'.join(pills), unsafe_allow_html=True)

def main():
    lang = detect_lang()
    labels = load_lang(lang)

    with st.sidebar:
        st.markdown(f\"### {labels.get('language_label','Language')}\")
        chosen = st.selectbox('', SUPPORTED, index=SUPPORTED.index(lang))
        if chosen != lang:
            set_lang(chosen)
            st.rerun()

    st.title(labels.get('title','Catholic Sacramentals'))
    st.write(labels.get('subtitle',''))

    items = load_items()
    all_label = labels.get('category_all','All')
    categories = [all_label] + sorted({it['category'] for it in items})

    current = st.query_params.get('cat', [all_label])[0]
    if current not in categories:
        current = all_label

    category_bar(categories, current, lang)

    q = st.text_input(labels.get('search_placeholder','Search'), '').strip().lower()

    def match(it):
        in_cat = (current == all_label) or (it['category'] == current)
        if not q:
            return in_cat
        combined = ' '.join([it.get('name',''), it.get('description',''), ' '.join(it.get('sources',[]))]).lower()
        return in_cat and (q in combined)

    filtered = [it for it in items if match(it)]
    st.caption(labels.get('showing','Showing {shown} of {total}').format(shown=len(filtered), total=len(items)))

    if not filtered:
        st.info(labels.get('no_results','No results'))
        return

    cols = st.columns(3)
    for i, it in enumerate(filtered):
        with cols[i % 3]:
            st.markdown(\"<div style='border:1px solid rgba(0,0,0,.08); border-radius:12px; padding:10px; background:white'>\", unsafe_allow_html=True)
            img = ASSETS / it.get('image','')
            if not img.exists():
                img = ASSETS / 'placeholder.jpg'
            st.image(str(img), use_container_width=True)
            st.subheader(it.get('name'))
            st.caption(it.get('category'))
            st.write(it.get('description'))
            if it.get('sources'):
                st.markdown('**Sources:**')
                for s in it.get('sources',[]):
                    st.markdown(f'- {s}')
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
