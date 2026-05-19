# agents.md — Vibe coding guide (Codex + VS Code)

## Formål
- Holde AI-agenten (Codex/ChatGPT) på sporet: mål, regler og kontekst.

## Projektmål (kort)
- Samme COVID-19 KPI’er på tværs af platforme (ArcGIS, Power BI, Python: Streamlit/Shiny/Dash).
- Enkle, hurtige demoer; minimér opsætning.

## Ground rules
- **Forklar før du skriver større mængder kode.**
- **Ingen destruktive bulk-ændringer** uden godkendelse.
- Følg PEP8, brug typer når det hjælper.
- Filstruktur og navne som i repoet her.
- Opdater `prompts.md` og `prompts2codex.md` ved hvert svar.
- Giv aldrig forslag til tøj eller påklædning.
- ArcGIS-arbejde skal som udgangspunkt løses med ArcGIS API for Python og bruge Living Atlas for geografiske datasæt, når det er muligt.
- Når PowerPoint-præsentationen opdateres (commit/push), skal linket i `docs/index.html` peges på den nye rå filversion.

## Kontekst (pin/copy til AI-chat)
- Rod: `arcgis/`, `powerbi/`, `python/` (3 platforme)
- Python apps: `python/streamlit_app/app.py`, `python/shiny_app/app.py`, `python/dash_app/app.py`
- Delte utils og data: `python/utils/`, `python/data/`

## Dataschema (placeholder)
- Kolonner: `date`, `level` ∈ {Global, EU, Nordic, DK}, `metric`, `value`
- CSV i `python/data/…` (indsættes senere)

## UI/Design
- Konsekvente KPI-navne og akser.
- Farver og labels ens på tværs.

## Sikkerhed
- Ingen nøgler/secrets i repo. Brug env-vars.

## Kommandoliste (Windows)
- Opret miljø: `Tasks: Install requirements` (Ctrl+Shift+P → “Run Task”)
- Kør apps: VS Code “Run and Debug”:
  - **Streamlit**, **Dash**, **Shiny**

## Prompt-skabeloner
**“Refactor utils”**  
> Gennemgå `python/utils/…` og foreslå 2 forbedringer. Forklar kort, lav små PR-venlige diffs.

**“Add KPI chart”**  
> Tilføj linjegraf for `metric="cases_7d"` i alle tre Python-apps. Vis legend og ens aksetitler.

**“Data adapter”**  
> Skriv en helper der indlæser CSV og standardiserer kolonner → pandas DataFrame.

