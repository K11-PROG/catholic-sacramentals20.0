import streamlit as st
import json, os, hashlib, datetime

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
    # UI strings
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
    # deterministic by date for a pleasant daily feature
    today = datetime.date.today().isoformat()
    idx = int(hashlib.sha1(today.encode()).hexdigest(), 16) % max(1, n)
    return idx

def main():
    st.set_page_config(page_title="Catholic Sacramentals Encyclopedia", layout="wide")
    items = load_items()
    trans = load_translations()

    # ---- Language selector ----
    lang = st.sidebar.selectbox("Language / Idioma / Langue", ["en","fr","es"], index=0)

    st.title("📖 " + t_ui("title", lang, trans))

    # ---- Favorites init ----
    if "favorites" not in st.session_state:
        st.session_state.favorites = set()

    # ---- Search & Filter ----
    left, right = st.columns([2,1])
    with left:
        query = st.text_input(t_ui("search", lang, trans))
    with right:
        categories = [t_ui("all", lang, trans)] + sorted(list({i["category"] for i in items}))
        category = st.selectbox(t_ui("category", lang, trans), categories)

    # ---- Featured today ----
    st.markdown(f"### 🌟 {t_ui('featured_today', lang, trans)}")
    fi = featured_index(len(items))
    fitem = items[fi]
    fname = t_item_name(fitem, lang, trans)
    col1, col2 = st.columns([1,2])
    with col1:
        safe_image(os.path.join(ASSETS, fitem["image"]), caption=fname)
    with col2:
        st.subheader(fname)
        st.markdown(f"*{fitem['category']}*")
        st.write(fitem["description"])

    st.divider()

    # ---- Apply search + filter ----
    def match(item):
        ok_cat = (category == t_ui("all", lang, trans)) or (item["category"] == category)
        if not query:
            return ok_cat
        q = query.lower().strip()
        hay = " ".join([item.get("name",""), item.get("description","")]).lower()
        return ok_cat and (q in hay)

    filtered = [i for i in items if match(i)]

    # ---- List items ----
    for it in filtered:
        iname = t_item_name(it, lang, trans)
        c1, c2 = st.columns([1,2])
        with c1:
            safe_image(os.path.join(ASSETS, it["image"]), caption=iname)
        with c2:
            st.subheader(iname)
            st.markdown(f"*{it['category']}*")
            st.write(it["description"])
            fav_key = it["slug"]
            is_fav = fav_key in st.session_state.favorites
            if is_fav:
                if st.button("⭐ " + t_ui("remove_fav", lang, trans), key="rm_"+fav_key):
                    st.session_state.favorites.remove(fav_key)
            else:
                if st.button("☆ " + t_ui("add_fav", lang, trans), key="add_"+fav_key):
                    st.session_state.favorites.add(fav_key)
        st.markdown("---")

    # ---- Show favorites ----
    st.subheader("⭐ " + t_ui("favorites", lang, trans))
    if st.session_state.favorites:
        st.write(", ".join([t_item_name(i, lang, trans) for i in items if i["slug"] in st.session_state.favorites]))
    else:
        st.write("—")

if __name__ == "__main__":
    main()
