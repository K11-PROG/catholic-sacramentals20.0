
import os, json
from PIL import Image, UnidentifiedImageError
import streamlit as st

st.set_page_config(page_title="Catholic Sacramentals (EN)", layout="wide")
DATA_PATH = "sacramentals.json"

@st.cache_data
def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def safe_image(path):
    try:
        img = Image.open(path)
        st.image(img, use_container_width=True)
    except (FileNotFoundError, UnidentifiedImageError, OSError):
        st.image(os.path.join("assets","placeholder.jpg"), use_container_width=True)

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] { background: #f3ecdb; }
.block-container { padding-top: 1.2rem; }
.card {
  background: #fffaf0; border: 1px solid #d9c7a2; border-radius: 14px;
  padding: 1rem 1rem 0.2rem 1rem; box-shadow: 0 2px 10px rgba(0,0,0,.08); height: 100%;
}
.card h3 { margin: 0.2rem 0 0.6rem 0; }
.badge {
  display: inline-block; font-size: .8rem; background: #efe4c8; border: 1px solid #d9c7a2;
  padding: .15rem .5rem; border-radius: 999px; margin-bottom: .5rem;
}
</style>
""", unsafe_allow_html=True)

st.title("📖 Catholic Sacramentals — English Edition")

q = st.text_input("Search title or summary…").strip().lower()
category = st.selectbox("Filter by category", ["All","Blessings","Devotional Objects","Devotional Prayer","Devotional Garments","Medals","Liturgical Objects"])

items = load_data()
if q:
    items = [x for x in items if q in x["title"].lower() or q in x["summary"].lower()]
if category != "All":
    items = [x for x in items if x["category"] == category]

cols = st.columns(3, gap="large")
for idx, item in enumerate(items):
    with cols[idx%3]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"### {item['title']}")
        st.markdown(f'<span class="badge">{item["category"]}</span>', unsafe_allow_html=True)
        safe_image(os.path.join("assets", item["image"]))
        st.write(f"**Summary:** {item['summary']}")
        with st.expander("Background & History"):
            st.write(item["history"])
        with st.expander("Theology & Practice"):
            st.write(item["theology"])
            st.write("**Common Usage:**")
            for u in item.get("usage", []):
                st.write(f"- {u}")
        if item.get("notes"):
            with st.expander("Notes & Variations"):
                st.write(item["notes"])
        st.markdown("</div>", unsafe_allow_html=True)

if not items:
    st.info("No results. Try clearing the search or choosing another category.")
