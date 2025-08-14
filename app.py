import streamlit as st
import json
import os
from pathlib import Path

st.set_page_config(page_title="Catholic Sacramentals", layout="wide")

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "data" / "sacramentals.json"
IMAGES_DIR = BASE_DIR / "assets" / "images"
ICONS_DIR = BASE_DIR / "assets" / "icons"
PLACEHOLDER = IMAGES_DIR / "placeholder.png"

@st.cache_data
def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def category_bar(categories, current):
    # Build a horizontal, scrollable icon bar using query params
    st.markdown("""
        <style>
        .cat-bar {
            display: flex;
            gap: 12px;
            overflow-x: auto;
            padding: 8px 0 2px 0;
            scrollbar-width: thin;
            -ms-overflow-style: none;
        }
        .cat-pill {
            text-align: center;
            min-width: 84px;
            padding: 6px 8px;
            border-radius: 12px;
            border: 1px solid rgba(0,0,0,0.08);
            background: rgba(255,255,255,0.6);
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
            transition: transform .05s ease;
            text-decoration: none;
            color: inherit;
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .cat-pill:hover { transform: translateY(-1px); }
        .cat-pill.selected {
            border-color: rgba(60, 60, 220, .25);
            box-shadow: 0 2px 6px rgba(60, 60, 220, .15);
            background: rgba(60, 60, 220, .06);
        }
        .cat-pill img {
            width: 38px; height: 38px; object-fit: contain;
            margin-bottom: 6px;
        }
        .cat-pill span { font-size: 12px; }
        </style>
    """, unsafe_allow_html=True)

    pills_html = ["<div class='cat-bar'>"]
    for cat in categories:
        key = cat.lower()
        icon = ICONS_DIR / f"{key}.png"
        selected_class = " selected" if cat == current else ""
        href = f"?cat={cat}"
        img_src = str(icon).replace(str(BASE_DIR) + os.sep, "")
        pills_html.append(
            f"""<a class='cat-pill{selected_class}' href='{href}'>
                    <img src='{img_src}' alt='{cat}' />
                    <span>{cat}</span>
                </a>"""
        )
    pills_html.append("</div>")
    st.markdown("\n".join(pills_html), unsafe_allow_html=True)

def main():
    st.title("📿 Catholic Sacramentals")
    st.write("Phase 1: Horizontal category bar with icons, 'All' option, combined search + filter, and image fallback.")

    items = load_data()

    categories = ["All"] + sorted({it["category"] for it in items})

    current = st.query_params.get("cat", ["All"])[0]
    if current not in categories:
        current = "All"

    category_bar(categories, current)

    q = st.text_input("Search (name or description)", "").strip().lower()

    def match(it):
        by_cat = (current == "All") or (it["category"] == current)
        if not q:
            return by_cat
        return by_cat and (q in it["name"].lower() or q in it["description"].lower())

    filtered = [it for it in items if match(it)]
    st.caption(f"Showing {len(filtered)} of {len(items)}")

    cols = st.columns(3)
    for i, it in enumerate(filtered):
        with cols[i % 3]:
            img_path = IMAGES_DIR / it.get("image", "")
            if not img_path.exists():
                img_path = PLACEHOLDER
            st.image(str(img_path), use_container_width=True)

            st.subheader(it["name"])
            cat_row = st.columns([1, 6])
            icon_path = ICONS_DIR / f"{it['category'].lower()}.png"
            with cat_row[0]:
                if icon_path.exists():
                    st.image(str(icon_path), use_container_width=True)
            with cat_row[1]:
                st.caption(it["category"])

            st.write(it["description"])

if __name__ == "__main__":
    main()
