
import streamlit as st
import json
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "sacramentals.json")
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

@st.cache_data
def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    st.title("Catholic Sacramentals")
    sacramentals = load_data()

    # Category filter
    categories = ["All"] + sorted(set(item["category"] for item in sacramentals))
    selected_category = st.selectbox("Filter by Category", categories)

    # Search box
    search_query = st.text_input("Search by name or description").lower()

    # Filtered items
    filtered_items = [
        item for item in sacramentals
        if (selected_category == "All" or item["category"] == selected_category)
        and (search_query in item["name"].lower() or search_query in item["description"].lower())
    ]

    for item in filtered_items:
        image_path = os.path.join(ASSETS_DIR, item["image"])
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)
        st.subheader(item["name"])
        st.write(f"**Category:** {item['category']}")
        st.write(item["description"])

if __name__ == "__main__":
    main()
