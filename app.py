import streamlit as st
import json
import os

DATA_PATH = os.path.join("data", "sacramentals.json")

def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    st.set_page_config(page_title="Catholic Sacramentals Encyclopedia", layout="wide")
    st.title("✝️ Catholic Sacramentals Encyclopedia")

    st.sidebar.header("Filter Sacramentals")
    category = st.sidebar.selectbox("Select Category", ["All", "Blessed Objects", "Devotional Items", "Prayers"])

    items = load_data()

    if category != "All":
        items = [item for item in items if item["category"] == category]

    for item in items:
        st.subheader(item["name"])
        img_path = os.path.join("assets", item["image"])
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        st.markdown(item["description"])
        st.markdown(f"**Category:** {item['category']}")
        st.markdown("---")

if __name__ == "__main__":
    main()
