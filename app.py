import streamlit as st
import json, os

DATA_PATH = os.path.join("data", "sacramentals.json")
FAV_PATH = "favorites.json"

st.set_page_config(page_title="Catholic Sacramentals", layout="wide")

# --- Load data ---
def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# --- Save favorites ---
def save_favorites(favs):
    with open(FAV_PATH, "w", encoding="utf-8") as f:
        json.dump(favs, f, indent=2)

def main():
    st.title("📖 Catholic Sacramentals Encyclopedia (Phase 5.2)")

    items = load_data()

    # Favorites
    if "favorites" not in st.session_state:
        st.session_state.favorites = []

    # Search
    query = st.text_input("🔍 Search sacramentals (press / to focus)", key="search")
    filtered = [i for i in items if query.lower() in i["name_en"].lower()]

    # Toggle view
    view = st.radio("View mode", ["Grid", "List"], horizontal=True)

    if view == "Grid":
        cols = st.columns(3)
        for idx, item in enumerate(filtered):
            with cols[idx % 3]:
                st.image(os.path.join("assets", item["image"]), use_container_width=True)
                st.markdown(f"**{item['name_en']}**")
                st.caption(item['desc_en'])
                if st.button("⭐ Favorite", key=f"fav_{idx}"):
                    if item['name_en'] not in st.session_state.favorites:
                        st.session_state.favorites.append(item['name_en'])
    else:
        for idx, item in enumerate(filtered):
            st.image(os.path.join("assets", item["image"]), width=120)
            st.markdown(f"### {item['name_en']}")
            st.write(item['desc_en'])
            if st.button("⭐ Favorite", key=f"fav_list_{idx}"):
                if item['name_en'] not in st.session_state.favorites:
                    st.session_state.favorites.append(item['name_en'])

    # Favorites section
    st.sidebar.subheader("⭐ Favorites")
    st.sidebar.write(st.session_state.favorites)
    if st.sidebar.button("💾 Export Favorites"):
        save_favorites(st.session_state.favorites)
        st.sidebar.success("Favorites exported to favorites.json")

if __name__ == "__main__":
    main()
