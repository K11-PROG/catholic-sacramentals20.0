
import streamlit as st
import os

st.set_page_config(page_title="Catholic Sacramentals Encyclopedia", layout="wide")

# Background style
page_bg = f"""
<style>
.stApp {{
    background-image: url("https://www.transparenttextures.com/patterns/parchment.png");
    background-size: cover;
    color: #2c1b0c;
}}
.card {{
    background: rgba(255, 248, 220, 0.9);
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.2);
}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

sacramentals = [
    {"name": "Holy Water", "desc": "Blessed water used for protection and blessing.", "image": "holy_water.jpg"},
    {"name": "Rosary", "desc": "Prayer beads used for meditations on Christ's life.", "image": "rosary.jpg"},
    {"name": "Scapular", "desc": "A devotional garment symbolizing Marian protection.", "image": "scapular.jpg"},
    {"name": "Crucifix", "desc": "A cross bearing the figure of Christ crucified.", "image": "crucifix.jpg"},
    {"name": "Medal of St. Benedict", "desc": "A sacramental medal invoking the intercession of St. Benedict.", "image": "st_benedict_medal.jpg"},
    {"name": "Palm Branches", "desc": "Blessed palms distributed on Palm Sunday.", "image": "palms.jpg"},
    {"name": "Ashes", "desc": "Imposed on Ash Wednesday as a sign of repentance.", "image": "ashes.jpg"},
    {"name": "Blessed Candles", "desc": "Used especially at Candlemas and during storms.", "image": "candle.jpg"},
    {"name": "Incense", "desc": "Burned as a symbol of prayers rising to God.", "image": "incense.jpg"},
    {"name": "Oil of the Sick", "desc": "Used in the Anointing of the Sick.", "image": "oil.jpg"},
    {"name": "Holy Cards", "desc": "Small devotional images with prayers.", "image": "holy_card.jpg"},
    {"name": "Relics", "desc": "Physical remains or belongings of saints.", "image": "relic.jpg"},
]

cols = st.columns(2)
for idx, item in enumerate(sacramentals):
    with cols[idx % 2]:
        st.markdown(f"<div class='card'><h3>{item['name']}</h3>", unsafe_allow_html=True)
        img_path = os.path.join("assets", item["image"])
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        else:
            st.image("assets/placeholder.jpg", use_container_width=True)
        st.write(item["desc"])
        st.markdown("</div>", unsafe_allow_html=True)
