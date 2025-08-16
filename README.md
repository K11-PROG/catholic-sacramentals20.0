# Catholic Sacramentals — Phase 5.1

**What's new**
- Auto-language detection (via browser) with fallback to English; still user-selectable.
- 12 sacramentals with extended descriptions and categories.
- Combined search + category filter.
- Favorites and a daily featured item.
- Valid small PNG images to avoid PIL errors.

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Query Param Override
Append `?lang=fr` or `?lang=es` to the app URL to force a language.

## Files
- `app.py` — Streamlit app
- `sacramentals.json` — data (12 items)
- `translations.json` — UI + name translations (EN/FR/ES)
- `assets/` — safe PNGs
- `requirements.txt`
