import streamlit as st
import os
import json

def load_data():
    with open(os.path.join("data", "sacramentals.json"), "r", encoding="utf-8") as f:
        return json.load(f)

def safe_image(path):
    try:
        st.image(path, use_container_width=True)
    except Exception:
        st.image(os.path.join("assets", "fallback.jpg"), use_container_width=True)

def main():
    st.set_page_config(page_title="Catholic Sacramentals Encyclopedia", layout="wide")
    st.title("📖 Catholic Sacramentals Encyclopedia")

    data = load_data()

    categories = ["All"] + sorted(set(item["category"] for item in data))
    selected_cat = st.sidebar.selectbox("Filter by Category", categories)

    if selected_cat == "All":
        filtered = data
    else:
        filtered = [item for item in data if item["category"] == selected_cat]

    for item in filtered:
        st.subheader(item["name"])
        img_path = os.path.join("assets", item["image"])
        safe_image(img_path)
        st.write(item["description"])

if __name__ == "__main__":
    main()
