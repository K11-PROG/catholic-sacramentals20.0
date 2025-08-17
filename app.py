import streamlit as st
import json, os

st.set_page_config(page_title='Catholic Sacramentals – Phase 5.3 (Light)', layout='wide')

DATA = 'data/sacramentals.json'
ASSETS = 'assets'
FALLBACK = os.path.join(ASSETS, 'fallback.jpg')

@st.cache_data
def load_items():
    with open(DATA, 'r', encoding='utf-8') as f:
        return json.load(f)

def safe_image(path: str):
    try:
        st.image(path, use_container_width=True)
    except Exception:
        st.image(FALLBACK, use_container_width=True)

def card(item):
    with st.container(border=True):
        st.markdown(f"### {item['name']}")
        img_path = os.path.join(ASSETS, item['image'])
        safe_image(img_path)
        st.markdown('**Origin / History**'); st.write(item['origin'])
        st.markdown('**Use in the Church**'); st.write(item['use'])
        st.markdown('**Variations**'); st.write(item['variations'])
        st.markdown('**Dates & Key Events**'); st.write(item['dates'])

def main():
    st.title('📖 Catholic Sacramentals Encyclopedia – Phase 5.3 (Light)')
    st.caption('Card layout • 12 core sacramentals • compact assets')
    items = load_items()
    q = st.text_input('🔎 Search by name', '')
    if q:
        items = [i for i in items if q.lower() in i['name'].lower()]
    cols = st.columns(2, vertical_alignment='top')
    for idx, it in enumerate(items):
        with cols[idx % 2]:
            card(it)

if __name__ == '__main__':
    main()
