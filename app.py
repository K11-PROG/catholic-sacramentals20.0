import streamlit as st
import json, os, hashlib, datetime, locale

try:
    from streamlit_javascript import st_javascript
    HAS_JS = True
except Exception:
    HAS_JS = False

DATA_FILE = "sacramentals.json"
TRANS_FILE = "translations.json"
ASSETS = "assets"

@st.cache_data
def load_items():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_translations():
    with open(TRANS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def t_ui(key, lang, trans):
    return trans.get("ui", {}).get(lang, {}).get(key, trans.get("ui", {}).get("en", {}).get(key, key))

def t_item_name(item, lang, trans):
    slug = item.get("slug")
    name = item.get("name", "")
    return trans.get("items", {}).get(slug, {}).get(lang, {}).get("name", name)

def safe_image(path, caption=""):
    if os.path.exists(path):
        try:
            st.image(path, use_container_width=True, caption=caption)
            return
        except Exception:
            pass
    st.image(os.path.join(ASSETS, "placeholder.png"), use_container_width=True, caption=caption)

def featured_index(n):
    today = datetime.date.today().isoformat()
    idx = int(hashlib.sha1(today.encode()).hexdigest(), 16) % max(1, n)
    return idx

def detect_lang():
    # priority: query param ?lang=xx -> JS navigator.language -> system default -> en
    qp = st.query_params.get("lang", None)
    if qp:
        return qp[0:2].lower()
    if HAS_JS:
        try:
            nav_lang = st_javascript("JSON.stringify(navigator.language || navigator.userLanguage)")
            if nav_lang and isinstance(nav_lang, str):
                return nav_lang[0:2].lower()
        except Exception:
            pass
    try:
        sys = locale.getdefaultlocale()[0] or ""
        if sys:
            return sys[0:2].lower()
    except Exception:
        pass
    return "en"

def main():
    st.set_page_config(page_title="Catholic Sacramentals Encyclopedia", layout="wide")
    items = load_items()
    trans = load_translations()

    auto_lang = detect_lang()
    lang = st.sidebar.selectbox("Language", ["en","fr","es"], index=["en","fr","es"].index(auto_lang) if auto_lang in ["en","fr","es"] else 0)
    st.title("📖 " + t_ui("title", lang, trans))

    # Favorites
    if "favorites" not in st.session_state:
        st.session_state.favorites = set()

    # Search + filter
    left, right = st.columns([2,1])
    with left:
        query = st.text_input(t_ui("search", lang, trans))
    with right:
        cats = [t_ui("all", lang, trans)] + sorted(list({i["category"] for i in items}))
        cat = st.selectbox(t_ui("category", lang, trans), cats)

    # Featured
    st.markdown(f"### 🌟 {t_ui('featured_today', lang, trans)}")
    fidx = featured_index(len(items))
    fitem = items[fidx]
    fname = t_item_name(fitem, lang, trans)
    c1, c2 = st.columns([1,2])
    with c1:
        safe_image(os.path.join(ASSETS, fitem["image"]), caption=fname)
    with c2:
        st.subheader(fname)
        st.markdown(f"*{fitem['category']}*")
        st.write(fitem["description"])
    st.divider()

    # Match function
    def match(it):
        ok_cat = (cat == t_ui("all", lang, trans)) or (it["category"] == cat)
        if not query:
            return ok_cat
        q = query.lower().strip()
        hay = " ".join([it.get("name",""), it.get("description","")]).lower()
        return ok_cat and (q in hay)

    filtered = [i for i in items if match(i)]

    for it in filtered:
        iname = t_item_name(it, lang, trans)
        a, b = st.columns([1,2])
        with a:
            safe_image(os.path.join(ASSETS, it["image"]), caption=iname)
        with b:
            st.subheader(iname)
            st.markdown(f"*{it['category']}*")
            st.write(it["description"])
            key = it["slug"]
            if key in st.session_state.favorites:
                if st.button("⭐ " + t_ui("remove_fav", lang, trans), key="rm_"+key):
                    st.session_state.favorites.remove(key)
            else:
                if st.button("☆ " + t_ui("add_fav", lang, trans), key="add_"+key):
                    st.session_state.favorites.add(key)
        st.markdown("---")

    st.subheader("⭐ " + t_ui("favorites", lang, trans))
    if st.session_state.favorites:
        fav_names = [t_item_name(i, lang, trans) for i in items if i["slug"] in st.session_state.favorites]
        st.write(", ".join(fav_names))
    else:
        st.write("—")

if __name__ == "__main__":
    main()
