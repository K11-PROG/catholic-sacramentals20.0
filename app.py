import streamlit as st
import base64
from pathlib import Path
from PIL import Image, UnidentifiedImageError

# Define paths
APP_DIR = Path(__file__).parent
ASSETS = APP_DIR / "assets"
BG_FILE = ASSETS / "bg_stained.jpg"  # create this image manually
PLACEHOLDER = ASSETS / "fallback.jpg"  # your existing placeholder

def set_background():
    if BG_FILE.exists():
        try:
            with open(BG_FILE, "rb") as img_file:
                img_b64 = base64.b64encode(img_file.read()).decode()
            st.markdown(f'''
                <style>
                .stApp {{
                    background-image: url("data:image/jpeg;base64,{img_b64}");
                    background-size: cover;
                    background-position: center;
                    background-attachment: fixed;
                }}
                .card {{
                    background: rgba(255,255,255,0.85);
                    border-radius: 15px;
                    padding: 1rem;
                    margin-bottom: 1rem;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                }}
                </style>
            ''', unsafe_allow_html=True)
            return
        except Exception:
            pass
    # Fallback if image missing or corrupted
    st.markdown('''
        <style>
        .stApp {
            background-color: #f7f0e6;
        }
        .card {
            background: white;
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 8px;
        }
        </style>
    ''', unsafe_allow_html=True)
