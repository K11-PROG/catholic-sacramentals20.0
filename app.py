import streamlit as st
import os

st.set_page_config(page_title="Catholic Sacramentals", layout="wide")

# Background and card styling
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Stained_glass_window_-_geograph.org.uk_-_323683.jpg/640px-Stained_glass_window_-_geograph.org.uk_-_323683.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .card {
        background: rgba(255,255,255,0.85);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }
    </style>
    """
    , unsafe_allow_html=True
)

sacramentals = [
    {"name": "Holy Water", "desc": "Used for blessings and protection, holy water is blessed by a priest and recalls baptism."},
    {"name": "Scapular", "desc": "A devotional garment signifying consecration to Mary and a commitment to Christian living."},
    {"name": "Rosary", "desc": "A string of beads used for meditative prayer on the life of Christ and Mary."},
    {"name": "Crucifix", "desc": "A cross with the body of Christ, symbolizing His sacrifice and victory over death."},
    {"name": "Medals", "desc": "Sacramental medals, like the Miraculous Medal or St. Benedict Medal, are worn for spiritual protection."},
    {"name": "Candles", "desc": "Lit during Mass, prayers, or vigils, symbolizing Christ as the Light of the World."},
    {"name": "Palms", "desc": "Blessed on Palm Sunday, palms are kept in homes as reminders of Christ’s Passion."},
    {"name": "Ashes", "desc": "Received on Ash Wednesday as a call to repentance: 'Remember you are dust, and to dust you shall return.'"},
    {"name": "Blessed Salt", "desc": "Salt blessed by a priest, used for protection and exorcism purposes."},
    {"name": "Relics", "desc": "Physical remains or objects associated with saints, venerated as holy reminders."},
    {"name": "Incense", "desc": "Burned during liturgies as a symbol of prayers rising to God."},
    {"name": "Holy Oils", "desc": "Sacred oils used in sacraments like Baptism, Confirmation, and Anointing of the Sick."}
]

st.title("✨ Catholic Sacramentals ✨")

# Display cards
for item in sacramentals:
    st.markdown(f"<div class='card'><h3>{item['name']}</h3><p>{item['desc']}</p></div>", unsafe_allow_html=True)
