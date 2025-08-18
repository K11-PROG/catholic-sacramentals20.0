import streamlit as st
import os

st.set_page_config(page_title="Catholic Sacramentals", layout="wide")

# Custom CSS for parchment background and card layout
st.markdown(
    '''
    <style>
    body {
        background-color: #fdf6e3;
        background-image: url("https://www.transparenttextures.com/patterns/parchment.png");
    }
    .sacramental-card {
        background: #fff8dc;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
    ''',
    unsafe_allow_html=True
)

def safe_image(img_path):
    try:
        st.image(img_path, use_container_width=True)
    except Exception:
        st.image(os.path.join("assets", "placeholder.jpg"), use_container_width=True)

# Core 12 sacramentals with extended descriptions
sacramentals = [
    {
        "title": "Holy Water",
        "image": "holy_water.jpg",
        "description": "Holy Water is water blessed by a priest or bishop, used for blessings, protection, and recalling baptism. Its use dates back to the early centuries of the Church, with references by St. Epiphanius (4th century)."
    },
    {
        "title": "Rosary",
        "image": "rosary.jpg",
        "description": "The Rosary is a string of beads used to meditate on the life of Christ and Mary. Popularized by St. Dominic in the 13th century after an apparition of the Blessed Virgin Mary."
    },
    {
        "title": "Scapular of Our Lady of Mount Carmel",
        "image": "scapular.jpg",
        "description": "The Brown Scapular, originating in the 13th century with St. Simon Stock, is a sign of devotion and Marian protection. Different scapulars exist, each tied to specific devotions."
    },
    {
        "title": "Crucifix",
        "image": "crucifix.jpg",
        "description": "The Crucifix, displaying Christ on the Cross, is a powerful sign of faith and protection. Early Christians used it as both a devotional item and an identity marker."
    },
    {
        "title": "Medal of St. Benedict",
        "image": "st_benedict_medal.jpg",
        "description": "The St. Benedict Medal includes Latin inscriptions of prayers of exorcism and protection. Its origins go back at least to the 17th century, though Benedictine devotion is older."
    },
    {
        "title": "Miraculous Medal",
        "image": "miraculous_medal.jpg",
        "description": "Given by the Virgin Mary to St. Catherine Labouré in Paris (1830), the Miraculous Medal is associated with countless graces and conversions."
    },
    {
        "title": "Ashes",
        "image": "ashes.jpg",
        "description": "Blessed ashes, imposed on Ash Wednesday, signify repentance and mortality. The custom is traceable to the 8th century but has biblical roots."
    },
    {
        "title": "Palm Branches",
        "image": "palms.jpg",
        "description": "Blessed palms from Palm Sunday recall Christ's triumphal entry into Jerusalem. They are often kept in homes until the next Lent, then burned for ashes."
    },
    {
        "title": "Blessed Candles",
        "image": "candle.jpg",
        "description": "Candles blessed at Candlemas (Feast of the Presentation, Feb 2) symbolize Christ as the Light of the World. Used in processions, prayer, and protection."
    },
    {
        "title": "Incense",
        "image": "incense.jpg",
        "description": "Blessed incense, used in liturgy, symbolizes prayers rising to heaven. Ancient Christian use mirrors Jewish Temple tradition."
    },
    {
        "title": "Agni Dei (Lamb of God wax discs)",
        "image": "agnus_dei.jpg",
        "description": "Wax discs blessed by Popes, imprinted with the Lamb of God, given at Easter. Popular from the 9th century onward, though largely discontinued after Vatican II."
    },
    {
        "title": "Blessed Salt",
        "image": "blessed_salt.jpg",
        "description": "Salt blessed by a priest is used in exorcisms, blessings, and recalling Christ’s words: 'You are the salt of the earth.' Its use is ancient, tied to baptismal rites."
    }
]

st.title("Catholic Sacramentals Encyclopedia")

for item in sacramentals:
    with st.container():
        st.markdown(f"<div class='sacramental-card'><h3>{item['title']}</h3></div>", unsafe_allow_html=True)
        safe_image(os.path.join("assets", item["image"]))
        st.write(item["description"])
