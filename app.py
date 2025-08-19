import streamlit as st
from pathlib import Path
import base64
from PIL import Image, UnidentifiedImageError
import io

st.set_page_config(page_title="Catholic Sacramentals", layout="wide")

# Paths
ASSETS = Path(__file__).parent / "assets"
BG = ASSETS / "bg_stained.jpg"
PLACEHOLDER = ASSETS / "placeholder.jpg"

# Load background and inject CSS into .stAppViewContainer
def load_bg():
    if BG.exists():
        try:
            data = base64.b64encode(BG.read_bytes()).decode()
            st.markdown(f'''
                <style>
                [data-testid="stAppViewContainer"] {{
                  background-image: url("data:image/jpeg;base64,{data}");
                  background-size: cover;
                  background-position: center;
                  background-attachment: fixed;
                }}
                .glass-card {{
                  background: rgba(255, 255, 255, 0.2);
                  backdrop-filter: blur(10px);
                  -webkit-backdrop-filter: blur(10px);
                  border-radius: 18px;
                  padding: 20px;
                  margin-bottom: 20px;
                  box-shadow: 0 4px 30px rgba(0,0,0,0.1);
                  border: 1px solid rgba(255, 255, 255, 0.3);
                }}
                .glass-top {{
                  background: rgba(255, 255, 255, 0.25);
                  backdrop-filter: blur(12px);
                  -webkit-backdrop-filter: blur(12px);
                  border-radius: 18px;
                  padding: 20px;
                  margin-bottom: 25px;
                  text-align: center;
                  font-size: 2rem;
                  font-weight: bold;
                  color: #212121;
                }}
                </style>
            ''', unsafe_allow_html=True)
            return
        except Exception:
            pass
    # Fallback (plain background)
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] { background-color: #f3ecdb; }
        .glass-card, .glass-top { background: white; padding: 1rem; border-radius: 10px; }
        </style>
    """, unsafe_allow_html=True)

# Safe image loader
def safe_image(name):
    img_path = ASSETS / name
    try:
        img = Image.open(img_path)
    except Exception:
        try:
            img = Image.open(PLACEHOLDER)
        except Exception:
            st.info(f"Missing image: {name}")
            return
    st.image(img, use_container_width=True)

# Run
load_bg()
st.markdown('<div class="glass-top">Catholic Sacramentals Encyclopedia</div>', unsafe_allow_html=True)

items = [
    {"name": "Holy Water", "desc": "Water blessed by a priest, used for protection and blessings.", "img": "holy_water.jpg"},
    {"name": "Rosary", "desc": "Beads used to meditate on the mysteries of Christ and Mary.", "img": "rosary.jpg"},
    {"name": "Scapular", "desc": "A devotional garment signifying consecration to Mary.", "img": "scapular.jpg"},
    {"name": "Crucifix", "desc": "Cross bearing Jesus, reminding us of His passion and love.", "img": "crucifix.jpg"},
]

# Responsive card layout
cols = st.columns(2)
for i, itm in enumerate(items):
    with cols[i % 2]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        safe_image(itm["img"])
        st.subheader(itm["name"])
        st.write(itm["desc"])
        st.markdown('</div>', unsafe_allow_html=True)
