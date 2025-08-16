# Catholic Sacramentals Encyclopedia — Phase 5

Streamlit app with search + category filter (combined), favorites, daily featured item, basic multilingual (EN/FR/ES), and small valid PNG assets.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Files
- `app.py` — Streamlit app
- `sacramentals.json` — core content
- `translations.json` — UI + item name translations (EN/FR/ES)
- `assets/` — valid PNG images + `placeholder.png`
- `requirements.txt` — dependencies

## Notes
- Favorites persist for the current session (Streamlit session_state).
- Search matches both name and description.
- Featured item is deterministic per day, not truly random.
