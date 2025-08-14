import streamlit as st
import json
import os

DATA_PATH = "data/sacramentals.json"
LANG_PATH = "data/lang"

@st.cache_data
def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_lang(lang_code):
    with open(os.path.join(LANG_PATH, f"{lang_code}.json"), "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    st.set_page_config(page_title="Catholic Sacramentals", layout="wide")

    # Language selector
    lang_code = st.sidebar.selectbox("Select Language", ["en", "fr"], index=0)
    lang = load_lang(lang_code)

    st.title(lang["title"])

    items = load_data()
    categories = sorted(set(item["category"] for item in items))
    categories.insert(0, lang["category_all"])

    selected_category = st.sidebar.selectbox("Category", categories)

    for item in items:
        if selected_category == lang["category_all"] or item["category"] == selected_category:
            st.subheader(item["name"])
            image_path = os.path.join("assets", "images", item["image"])
            if os.path.exists(image_path):
                st.image(image_path, use_container_width=True)
            st.write(item["description"])

if __name__ == "__main__":
    main()
