import streamlit as st
import json
import os

DATA_PATH = os.path.join("data", "sacramentals.json")

def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    st.set_page_config(page_title="Catholic Sacramentals", layout="wide")
    st.title("Catholic Sacramentals")

    # Search
    search_query = st.text_input("Search sacramentals")

    data = load_data()
    for item in data:
        if search_query.lower() in item["name"].lower() or search_query == "":
            st.subheader(item["name"])
            img_path = os.path.join("assets", "images", item["image"])
            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            else:
                st.write("[Image missing]")
            st.write(item["description"])

if __name__ == "__main__":
    main()
