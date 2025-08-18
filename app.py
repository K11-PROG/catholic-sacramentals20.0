import streamlit as st
import os

# Page config
st.set_page_config(page_title="Catholic Sacramentals Encyclopedia", layout="wide")

# Custom background (parchment style)
page_bg = f"""
<style>
.stApp {{
    background-image: url("https://i.ibb.co/VBfM7Wq/parchment-bg.jpg");
    background-size: cover;
    background-attachment: fixed;
    color: #2c2c2c;
}}
.card {{
    background-color: rgba(255, 255, 245, 0.9);
    border-radius: 15px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    padding: 1.5em;
    margin: 1em 0;
    text-align: center;
}}
.card img {{
    border-radius: 10px;
    max-height: 200px;
    object-fit: contain;
}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Language selector
lang = st.sidebar.selectbox("🌍 Language", ["English", "French", "Spanish", "Italian", "Tagalog"])

# Sacramentals data (core 12 with translations)
sacramentals = [
    {
        "key": "holy_water",
        "image": "holy_water.jpg",
        "translations": {
            "English": {"title": "Holy Water", "desc": "Blessed water used in sacramental rites, symbolizing purification and protection."},
            "French": {"title": "Eau Bénite", "desc": "Eau bénite utilisée dans les rites sacramentels, symbole de purification et de protection."},
            "Spanish": {"title": "Agua Bendita", "desc": "Agua bendita utilizada en los ritos sacramentales, símbolo de purificación y protección."},
            "Italian": {"title": "Acqua Benedetta", "desc": "Acqua benedetta usata nei riti sacramentali, simbolo di purificazione e protezione."},
            "Tagalog": {"title": "Banal na Tubig", "desc": "Binasbasang tubig na ginagamit sa mga sakramental na ritwal, sagisag ng paglilinis at proteksiyon."}
        }
    },
    {
        "key": "rosary",
        "image": "rosary.jpg",
        "translations": {
            "English": {"title": "Rosary", "desc": "A string of beads used for prayer and meditation on the life of Christ and Mary."},
            "French": {"title": "Chapelet", "desc": "Un chapelet de perles utilisé pour la prière et la méditation sur la vie du Christ et de Marie."},
            "Spanish": {"title": "Rosario", "desc": "Un conjunto de cuentas usado para la oración y meditación sobre la vida de Cristo y María."},
            "Italian": {"title": "Rosario", "desc": "Una serie di grani usata per la preghiera e la meditazione sulla vita di Cristo e Maria."},
            "Tagalog": {"title": "Rosaryo", "desc": "Isang tali ng mga butil para sa panalangin at pagbubulay sa buhay ni Kristo at Maria."}
        }
    }
]

# Display cards
cols = st.columns(3)
for i, item in enumerate(sacramentals):
    with cols[i % 3]:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        img_path = os.path.join("assets", item["image"])
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        else:
            st.image("https://via.placeholder.com/300x200.png?text=Image+Missing", use_container_width=True)
        st.subheader(item["translations"][lang]["title"])
        st.write(item["translations"][lang]["desc"])
        st.markdown("</div>", unsafe_allow_html=True)
