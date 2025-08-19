
import streamlit as st
import os

# Page config
st.set_page_config(page_title="Catholic Sacramentals", layout="wide")

# Custom glassmorphism CSS with stained glass background
st.markdown(
    """
    <style>
    body {
        background-image: url('https://upload.wikimedia.org/wikipedia/commons/6/6f/Chartres_Cathedral_Stained_Glass.jpg');
        background-size: cover;
        background-position: center;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 20px;
        margin-bottom: 20px;
    }
    .glass-topbar {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 15px;
        margin-bottom: 30px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        color: white;
        text-shadow: 1px 1px 4px rgba(0,0,0,0.6);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Top navigation bar
st.markdown('<div class="glass-topbar">Catholic Sacramentals Encyclopedia</div>', unsafe_allow_html=True)

# Example sacramentals
sacramentals = [
    {"name": "Holy Water", "description": "Water blessed by a priest, used as a sacramental for protection and blessing."},
    {"name": "Rosary", "description": "A devotion in honor of the Virgin Mary, consisting of a set number of prayers."},
    {"name": "Scapular", "description": "A sign of devotion and protection, worn around the neck."},
]

# Display cards
for item in sacramentals:
    st.markdown(f'<div class="glass-card"><h3>{item["name"]}</h3><p>{item["description"]}</p></div>', unsafe_allow_html=True)
