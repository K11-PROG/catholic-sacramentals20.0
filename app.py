import streamlit as st
import os

st.set_page_config(page_title="Catholic Sacramentals", layout="wide")

# CSS for background and glassmorphism
st.markdown(
    f"""
    <style>
    body {{
        background-image: url('assets/stained_glass.jpg');
        background-size: cover;
        background-attachment: fixed;
    }}
    .glass-bar {{
        background: rgba(255, 255, 255, 0.25);
        border-radius: 12px;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 15px;
        margin-bottom: 20px;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        color: #2c2c2c;
    }}
    .sacramental-card {{
        background: rgba(255, 255, 255, 0.55);
        border-radius: 16px;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 20px;
        margin: 15px;
        color: #1a1a1a;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }}
    </style>
    <div class="glass-bar">✨ Catholic Sacramentals Encyclopedia ✨</div>
    """,
    unsafe_allow_html=True
)

sacramentals = [
    {"name": "Holy Water", "desc": "Blessed water used for protection, blessings, and reminding of baptism.", "image": "placeholder.jpg"},
    {"name": "Rosary", "desc": "A prayer rope with beads, used for meditative prayer to Mary and Christ.", "image": "placeholder.jpg"},
    {"name": "Scapular", "desc": "A devotional garment symbolizing consecration to Mary and trust in her protection.", "image": "placeholder.jpg"},
]

cols = st.columns(3)
for idx, item in enumerate(sacramentals):
    with cols[idx % 3]:
        st.markdown(f"<div class='sacramental-card'><h3>{item['name']}</h3><p>{item['desc']}</p></div>", unsafe_allow_html=True)
        img_path = os.path.join("assets", item["image"])
        st.image(img_path, use_container_width=True)
