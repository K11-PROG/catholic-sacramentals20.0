import streamlit as st
import json
import os

ASSETS_DIR = "assets"

def safe_image(img_path, caption=""):
    if os.path.exists(img_path):
        try:
            st.image(img_path, use_container_width=True, caption=caption)
        except Exception:
            st.warning(f"⚠️ Could not load image: {img_path}")
            st.image(os.path.join(ASSETS_DIR, "placeholder.png"), use_container_width=True, caption=caption)
    else:
        st.warning(f"⚠️ Missing image: {img_path}")
        st.image(os.path.join(ASSETS_DIR, "placeholder.png"), use_container_width=True, caption=caption)

@st.cache_data
def load_data():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    st.title("📖 Catholic Sacramentals Encyclopedia")
    items = load_data()

    categories = ["All"] + sorted(set(item["category"] for item in items))
    choice = st.sidebar.selectbox("Filter by Category", categories)

    if choice != "All":
        items = [item for item in items if item["category"] == choice]

    for item in items:
        st.subheader(item["name"])
        safe_image(os.path.join(ASSETS_DIR, item["image"]), caption=item["name"])
        st.write(item["description"])

if __name__ == "__main__":
    main()
