# ArcGIS workflow til Dansk Esri Konference 2026

- Gem exports og konfigurationer i `arcgis/dashboards/`.
- Dokumentér webmaps/feature layers og deling (organisation/offentlig).
- Forvent, at ArcGIS Online-licens er tilgængelig, og opret alle nye items i mappen `dek_2026`.
- Brug ArcGIS API for Python som primær værktøjskæde til opsætning, publicering og opdatering.
- Vælg Living Atlas som standardkilde til geografiske datasæt (landegrænser m.m.), når det er muligt.

## Miljø

- Brug ArcGIS Pro Python eller opret et separat virtuelt miljø til ArcGIS-arbejde:
  ```powershell
  python -m venv .venv_arcgis
  .\.venv_arcgis\Scripts\activate
  pip install -r requirements.txt
  ```
- Har du ArcGIS Pro installeret og er allerede logget ind dér, kan scripts køres med ArcGIS Pro’s Python (inkl. `arcpy`) uden særskilt login:
  ```powershell
  "C:\Program Files\ArcGIS\Pro\bin\Python\Scripts\propy.bat" arcgis\dashboards\create_nordic_covid_scene.py
  "C:\Program Files\ArcGIS\Pro\bin\Python\Scripts\propy.bat" arcgis\dashboards\create_nordic_covid_dashboard.py
  ```

## Dashboard

- `create_nordic_covid_dashboard.py` finder hosted feature layeret fra 3D-scenen, opretter et webkort og opretter eller opdaterer et ArcGIS Dashboards item.
- Dashboardet er tænkt som det Esri-native overblik ved siden af 3D-scenen.
- Åbn dashboardet i ArcGIS Online efter scriptkørsel for at finjustere layout, selectors og deling.

## Population reference

- 2022-befolkningstal bruges i den nordiske COVID-19 scene og ligger i `data/nordic_population_2022.csv`.
- Kilder (officiel statistik):
  - Danmark: Statistics Denmark (Population 1 January 2022)
  - Finland: Statistics Finland (Population structure 31 December 2022)
  - Island: Statistics Iceland (Population 1 January 2022)
  - Norge: Statistics Norway (Population 1 January 2022)
  - Sverige: Statistics Sweden (Year-end population 2022)
