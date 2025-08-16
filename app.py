import streamlit as st
import json
import os

DATA_PATH = "sacramentals.json"
ASSETS_DIR = "assets"

def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    st.set_page_config(page_title="Catholic Sacramentals Encyclopedia", layout="wide")
    st.title("📖 Catholic Sacramentals Encyclopedia")

    items = load_data()

    categories = ["All"] + sorted(set(item["category"] for item in items))
    selected_category = st.sidebar.selectbox("Filter by Category", categories)

    for item in items:
        if selected_category == "All" or item["category"] == selected_category:
            st.subheader(item["name"])
            img_path = os.path.join(ASSETS_DIR, item["image"])
            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            st.write(item["description"])
            st.markdown("---")

if __name__ == "__main__":
    main()
