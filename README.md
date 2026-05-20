# Vibe coding · ArcGIS dashboards (Dansk Esri Konference 2026)

Dette repository samler materiale til Dansk Esri Konference 2026 om vibe coding og AI-assisteret udvikling af geodata-dashboards med Esri-teknologi. De tidligere ikke-Esri-demoer er fjernet, så repoet nu fokuserer på ArcGIS Online, ArcGIS API for Python, ArcGIS Dashboards og ArcGIS 3D.

## Struktur

- `arcgis/` – scripts og dokumentation til hosted feature layers, webkort, ArcGIS Dashboards og 3D-webscenen.
- `data/` – datagrundlag brugt af ArcGIS-scriptet (OWID, SSI, geometri og populationstal).
- `docs/` – statiske filer som publiceres via GitHub Pages.
- `praesentation.md` – outline til oplægget.
- `prompts.md` / `prompts2codex.md` – promptlog og udviklingsnoter fra arbejdet.

## Kom godt i gang

1. Brug et ArcGIS Pro Python-miljø eller et miljø med ArcGIS API for Python:
   ```powershell
   "C:\Program Files\ArcGIS\Pro\bin\Python\Scripts\propy.bat" arcgis\dashboards\create_nordic_covid_scene.py
   ```
2. Alternativt opret et separat miljø:
   ```powershell
   python -m venv .venv_arcgis
   .\.venv_arcgis\Scripts\activate
   pip install -r requirements.txt
   ```
3. Log ind i ArcGIS Pro eller konfigurer en `home`/`pro` profil, så `GIS("pro")` eller `GIS("home")` virker.

### Fejlfinding: NumPy 2 i ArcGIS Pro clone

Hvis `from arcgis.gis import GIS` viser fejl som `_ARRAY_API not found` eller
`A module that was compiled using NumPy 1.x cannot be run in NumPy 2.x`, er
miljoet blandet med NumPy 2 og binaere pakker bygget mod NumPy 1.x. Pin eller
nedgrader NumPy i det aktive ArcGIS-miljo:

```powershell
conda activate arcgispro-py3-clone
conda install "numpy<2"
```

Koer derefter dashboard-scriptet igen fra samme miljo.

## ArcGIS workflow

- `arcgis/dashboards/create_nordic_covid_scene.py` opretter eller opdaterer et tidsaktiveret hosted feature layer og en 3D-webscene med nordiske COVID-19 KPI'er.
- `arcgis/dashboards/create_nordic_covid_dashboard.py` opretter et ArcGIS Dashboards item baseret på samme hosted feature layer.
- Begge scripts placerer output i ArcGIS Online-mappen `dek_2026`.
- Datasæt og populationstal ligger i `data/` og dokumenteres i `arcgis/README.md`.

## GitHub Pages

- `docs/index.html` er landingssiden med links til præsentation, ArcGIS 3D-webscene og ArcGIS Dashboard workflow.
- `docs/scene.html` embedder webscenen.
- `docs/esri-dashboard.html` beskriver dashboard-scriptet og outputtet.
- `docs/praesentation.html` loader `praesentation.md` og viser oplæggets outline.
- Publicér via **GitHub Pages -> Deploy from branch** (vælg branch og `/docs`). Lokal test: `python -m http.server --directory docs` og åbn `http://localhost:8000/`.

## Licens og attribution

- Projektet er licenseret under **CC BY-NC-SA 4.0** (se `LICENSE`).
- Eksterne datasæt (OWID, SSI, nationale statistik-kilder m.fl.) refereres i dokumentation og scripts.
