
import streamlit as st, json, os, base64, urllib.parse
from pathlib import Path
try:
    from streamlit_javascript import st_javascript
    HAS_JS = True
except Exception:
    HAS_JS = False

BASE = Path(__file__).parent
DATA = BASE / "data" / "sacramentals_full.json"
TRANS = BASE / "data" / "translations_full.json"
ASSETS = BASE / "assets"
FALLBACK = ASSETS / "fallback.jpg"

@st.cache_data
def load_items():
    with open(DATA, "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_trans():
    with open(TRANS, "r", encoding="utf-8") as f:
        return json.load(f)

def detect_lang(default="en"):
    qp = st.query_params.get("lang", None)
    if qp:
        return qp[0:2].lower()
    if HAS_JS:
        try:
            nav = st_javascript("return navigator.language || navigator.userLanguage || null;")
            if isinstance(nav, str):
                return nav.split("-")[0]
        except Exception:
            pass
    try:
        import locale
        sys = locale.getdefaultlocale()[0]
        if sys:
            return sys.split("_")[0]
    except Exception:
        pass
    return default

def safe_image(path):
    try:
        st.image(str(path), use_container_width=True)
    except Exception:
        st.image(str(FALLBACK), use_container_width=True)

def encode_favorites(favs):
    b = json.dumps(favs, ensure_ascii=False).encode("utf-8")
    return base64.urlsafe_b64encode(b).decode("utf-8")

def decode_favorites(token):
    try:
        b = base64.urlsafe_b64decode(token.encode("utf-8"))
        return json.loads(b.decode("utf-8"))
    except Exception:
        return []

def main():
    st.set_page_config(page_title="Catholic Sacramentals Full", layout="wide")
    items = load_items()
    trans = load_trans()

    lang_auto = detect_lang()
    langs = ["en","fr","es","it","tl"]
    lang = st.sidebar.selectbox("Language", langs, index=langs.index(lang_auto) if lang_auto in langs else 0)
    ui = trans.get("ui", {}).get(lang, trans.get("ui", {}).get("en", {}))

    st.title(ui.get("title", "Catholic Sacramentals"))
    # search + category
    q = st.text_input(ui.get("search","Search"), key="search_input")
    cats = [ui.get("all","All")] + sorted(list({it["category"] for it in items}))
    cat = st.sidebar.selectbox(ui.get("category","Category"), cats)

    # view toggle
    view = st.sidebar.radio(ui.get("view","View"), ("Grid","List"))

    # favorites init
    if "favorites" not in st.session_state:
        st.session_state.favorites = []

    # featured
    st.markdown("### 🌟 " + ui.get("featured_today","Featured Today") if ui.get("featured_today") else "Featured Today")

    # filter items
    def match(it):
        ok_cat = (cat == ui.get("all","All")) or (it["category"] == cat)
        if q:
            ql = q.lower()
            hay = " ".join([it.get("name",""), it.get("origin",""), it.get("use","")]).lower()
            return ok_cat and (ql in hay)
        return ok_cat

    filtered = [it for it in items if match(it)]

    # render items
    if view == "Grid":
        cols = st.columns(3)
        for idx, it in enumerate(filtered):
            col = cols[idx % 3]
            with col:
                st.header(it["name"])
                safe_image(ASSETS / it["image"])
                st.write(it["origin"])
                st.write(it["use"])
                if st.button(("⭐ Remove" if it["slug"] in st.session_state.favorites else "☆ Add") + " " + ui.get("favorites","Favorites"), key="fav_"+it["slug"]):
                    if it["slug"] in st.session_state.favorites:
                        st.session_state.favorites.remove(it["slug"])
                    else:
                        st.session_state.favorites.append(it["slug"])
    else:
        for it in filtered:
            st.header(it["name"])
            safe_image(ASSETS / it["image"])
            st.markdown("**Origin / History**")
            st.write(it["origin"])
            st.markdown("**Use in the Church**")
            st.write(it["use"])
            st.markdown("**Variations**")
            st.write(it["variations"])
            st.markdown("**Dates & Key Events**")
            st.write(it["dates"])
            if st.button(("⭐ Remove" if it["slug"] in st.session_state.favorites else "☆ Add") + " " + ui.get("favorites","Favorites"), key="fav_"+it["slug"]):
                if it["slug"] in st.session_state.favorites:
                    st.session_state.favorites.remove(it["slug"])
                else:
                    st.session_state.favorites.append(it["slug"])

    # favorites panel
    st.sidebar.subheader(ui.get("favorites","Favorites"))
    fav_list = [next((x for x in items if x["slug"]==s), None) for s in st.session_state.favorites]
    fav_names = [f["name"] for f in fav_list if f]
    st.sidebar.write(", ".join(fav_names) if fav_names else "—")

    # export favorites
    if st.sidebar.button(ui.get("export","Export Favorites")):
        token = encode_favorites(st.session_state.favorites)
        st.sidebar.success("Favorites exported (URL token below).")
        st.sidebar.text_area("Share token (copy):", token, height=60)

    # import favorites via token
    token_input = st.sidebar.text_input(ui.get("share","Share Favorites"))
    if token_input:
        new = decode_favorites(token_input.strip())
        if isinstance(new, list):
            st.session_state.favorites = new
            st.sidebar.success("Favorites loaded from token.")

if __name__ == '__main__':
    main()
