
import streamlit as st
import os

st.set_page_config(page_title="Catholic Sacramentals", layout="wide")

# Custom stained glass background
page_bg = f'''
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-image: url("file://{os.path.join("assets","bg_stained.jpg")}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}
.block-container {{
    background: rgba(255,255,255,0.8);
    border-radius: 15px;
    padding: 2rem;
}}
</style>
'''
st.markdown(page_bg, unsafe_allow_html=True)

st.title("Catholic Sacramentals")

sacramentals = [
    {"name": "Holy Water", "desc": "Used for blessings and protection in the Catholic Church.", "image": "placeholder.jpg"},
    {"name": "Rosary", "desc": "Prayer beads to meditate on the life of Christ and the Virgin Mary.", "image": "placeholder.jpg"},
]

for item in sacramentals:
    st.subheader(item["name"])
    st.image(os.path.join("assets", item["image"]), use_container_width=True)
    st.write(item["desc"])
    st.divider()
