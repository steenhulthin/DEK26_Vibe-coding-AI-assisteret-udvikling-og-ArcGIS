# Prompts to Codex

1. Jeg har brug for covid-19 data på globalt niveau. Hvor kan jeg downloade det?
2. Lad os fokusere på indlæggelser og dødsfald. Kan du lægge data fra OWID og fra ECDC i datamappen (i et format der er læsbart med pandas)?
3. Jeg kan ikke se der er lavet et python venv? Kan du gøre det?
4. Ok, lad os fortsætte med at få hentet data.
5. Lad os også lige få hentet det danske data fra SSI: https://sseruminstitut.maps.arcgis.com/sharing/rest/content/items/67a8aedc7ff9466e8920951540c2097f/data
6. Lad os skære ned på datamængden i OWID datasættet. Behold kolonner med geografisk placering, indlæggelser og død.
7. Commit datafilerne, men dog ikke ssi_denmark_data.zip - ignorer den i stedet.
8. Kan du lave en prompts2codex.log (eller .md alt efter hvad der giver bedst mening) i roden af projektet. Den skal indeholde de prompts, jeg har givet dig.
9. Perfekt. Commit den.
10. Push både til github og origin.
11. Jeg vil bruge GitHub Pages til at hoste python dashboardsene (er det muligt med dash - det burde være muligt med shiny via shinylive og med streamlit via stlite). Kan du gøre en docs mappe klar til ghpages?
12. Det lyder godt. Lad os lave dashboards. Lad os starte med Streamlit. Streamlit skal være med OWID data. Der skal øverst være et kort over verden. Landene skal være farvet efter indlæggelser per capita og skraveret efter dødsfald per capita (hvis det er muligt). Der skal være en periodevælger, hvor der kan vælges år og måned. Tallene skal summeres over den valgte periode. Det skal være muligt at vælge et specifikt land. Under kortet skal der være en graf der viser indlæggelser og død per capita over tid (summeret på månedsniveau) for det valgte land (og ellers for hele verden).
13. Make it so!
14. Kan du starte streamlit?
15. Ok, tilføj streamlit til requirement og installér i venv.
16. Ja, kør den.
17. Jeg får en lang fejl, men jeg tror noget går galt med choropleth: (fejltrace).
18. Start serveren igen, så ser vi.
19. Så fint. Commit det.
20. Lad os lige få stlite til at fungere og se det i ghpages.
21. Serveren kører og jeg ser index.html siden, men jeg får: Fejl under indlæsning: stlite is not defined.
22. Ok, nu får jeg dog: Fejl under indlæsning: The `entrypoint` field is required.
23. Hvor lang tid forventer du det tager at loade?
24. Ok, vi skal måske tænke på stream.app hosting. Nå, kan du løbende tilføje mine prompts til prompts2codex? og lige tilføje de manglende i hvert fald.
25. Nå, min computer gik ned (ikke relateret til projektet). Kan vi lave et datasæt til streamlit dashboardet, som er præaggregeret på månedsniveau?
26. Ja, lad os se om det ikke bare er sagen. :) Og lad mig lige få kommandoen til at serve stlite på den lokale webserver igen også.
27. Husk at få tilføjet prompts til prompt-loggen. ;)
28. Hm, det ser ud som om det hænger. Bruger det det reducerede datasæt?
29. ::ffff:127.0.0.1 - - [24/Oct/2025 19:32:43] "GET / HTTP/1.1" 200 - (::ffff:127.0.0.1 - - [24/Oct/2025 19:32:45] "GET /python/streamlit_app/app.py HTTP/1.1" 200 - ::ffff:127.0.0.1 - - [24/Oct/2025 19:32:45] "GET /python/data/owid_covid_global_monthly.csv HTTP/1.1" 200 - ::ffff:127.0.0.1 - - [24/Oct/2025 19:32:45] code 404, message File not found ::ffff:127.0.0.1 - - [24/Oct/2025 19:32:45] "GET /favicon.ico HTTP/1.1" 404 -)
30. Ok, der sker ikke noget. Men prøv at pushe til begge remotes. Jeg har slået ghpages til, så måske fungerer det der.
31. Drevet var blevet disconnected. Tilføj lige prompt logs, commit og push igen.
32. Det starter ikke op i ghpages heller. Du skal lave startsiden, så den er ren html og har et link en side med stlite-delen.
33. Jeg har prøvet at lave en https://vibe-coding-kortdage-2025.streamlit.app/ app men den giver følgende fejl: File "//mount/src/vibe-coding-kortdage-2025/python/streamlit_app/app.py", line 2, in <module> import plotly.graph_objects as go
34. Kan det tænkes at requirements ikke kommer korrekt med?
35. Det kører fint på streamlit.app, men der sker ikke noget i stlite. Kan vi få en log, så vi har med muligheder for fejlfinding?
36. Genstart alle webservere
37. Jeg kan ikke se en log. Men lad det ligge for nuværende. Lad os få lavet en shiny eller dash app. Jeg vil gerne have en app med et kort over Danmark inddelt i regioner. Kortet skal vise et timelapse over indlæggelser over tid baseret på det danske data. Tænker du Dash eller shiny til den opgave?
38. Jeg får ModuleNotFoundError: No module named 'utils' når jeg kører python python/dash_app/app.py
39. App'en finder ikke datafilen: FileNotFoundError: ... \\vibe_coding\\data\\ssi_denmark\\03_bekraeftede...csv
40. Jeg har lagt regioner.geojson i python/data/. Brug den i stedet for demo-geojsonen.
41. Lav en simplificeret geojson ud fra regioner.geojson (fjern ca. 90 % af punkterne) og brug den i Dash.
42. Der vises en bounding box i Dash efter simplificering - juster simplificeringen så polygonerne bevares.
43. Rul tilbage til den simple geojson i Dash, men gem begge nye geojson-filer.
44. Brug regioner_simplified.geojson igen (den skal matche SSI-data og ikke vise bounding box).
45. Lav en denmark_regions_simple.geojson med samme struktur som den simple fil men med geometrier fra regioner_simplified, og brug den i Dash.
46. Jeg vil gerne have noget, hvor et kort over data er det centrale.
47. Det lyder godt, generér koden.
48. Husk også at opdatere prompts2codex.md filen.
49. Start med at bruge denmark_regions_simple.geojson til kortet.
50. Brug en shinypy version der understøtter sidebar og opdater layoutet derefter.
51. Sørg for at hoveddelen fylder resten, kortet (med seneste tal til højre) og grafen under med fuld bredde.
52. Fjern seneste tal-boksen og lad kortet fylde hele bredden; grafen skal stadig ligge under.
53. Sørg for at x-aksen i grafen vises som dato (ingen scientific notation).
54. Tilføj en lodret linje i grafen, der følger den valgte dato.
55. Udbyg ArcGIS scenen til månedlige data, brug vector-tile light gray basemap og publicér via propy.
56. Opdater prompt-loggen. Den skal være gemt i UTF-8.
57. Opdater logs, commit og push begge remotes.
58. Tilføj befolkningstal fra officielle kilder til arcgis scenen og beregn dødelighed pr 100.000.
59. Opdater logs og lav commit/push.
60. Embed webscenen i et ArcGIS dashboard eller experience med tids-slider og metadata.
61. Vurder om dashboard-API’et er brugbart og foreslå plan uden at skrive kode.
62. Lav en statisk GH Pages-side til webscenen og opdater prompt-logs.
63. Tilføj et link fra `docs/index.html` til den nye `docs/scene.html`.
64. Ret Living Atlas-referencen i scenesiden til et offentligt tilgængeligt link.
65. Peg Living Atlas-kilden mod FeatureServer-endpointet i scene-siden og dokumentationen.
66. Ret embed-parametre så webscenen vises i 3D med tidsregulator.
67. Opdater scene-siden til at bruge Instant App 3D Viewer (eller Scene Viewer fallback) og log ændringen.
68. Afklar Power BI-licenser, publicering og map-visuals (slået fra i desktop).
69. Forsøg med Power BI Filled Map og manglende farve/slicer-felter; beslutning om at publicere trods begrænsninger.
70. Eksportér Shiny-dashboard til Shinylive, link fra index og opdater dokumentation/logs.
71. Fix Shinylive filfejl ved at bundle SSI/geojson-data i appen, opdatere data-path fallback og regenerere export.
72. Opret `todo.md` i roden med næste skridt (geometrier, forsider, licens, hosting m.m.).
73. Tilføj CC BY-NC-SA 4.0 licens og markér TODO-punktet som udført.
74. Opret pros_cons.md med AI-fokuseret sammenligning af Shiny, Dash, Streamlit, ArcGIS 3D og Power BI.
75. Juster pros_cons.md: Power BI som mindre god (opsætning/AI) og fjern visuel fleksibilitet.
76. Tilføj i `agents.md` en regel om at opdatere `prompts.md` og `prompts2codex.md` efter hvert svar.
77. Bekræft at den nye regel er aktiv og registreret.
78. Stage, commit og push alle ændringer undtagen `praesentation.md`.
79. Gennemgå præsentation og abstract, foreslå forbedringer og stille opklarende spørgsmål.
80. Tilføj "ingen tøjforslag"-regel, commit/push og omstrukturér præsentationen med ekstra slides.
81. Afklar mulighed for at genskabe tidligere `praesentation.md`-version; kræver manuel kopi da filen aldrig blev committed.
82. Byg SSI-inspireret styling, markdown-baseret præsentationsside og opdateret docs-forside med præsentationslink.
83. Fix klikbare links ved at deaktivere overlay-pointer-events, tilføj `docs/praesentation.md` og opdater loaderens fallback-rækkefølge.
84. Opdater SRI-hash for Marked-scriptet, så markdown-parseren loader uden fejl.
85. Erstat CDN-afhængighed med lokal `assets/js/marked.min.js` (simpel parser) og opdater præsentationssiden.
86. Udfyld præsentationsslides med prompteksempler (Streamlit, Shiny, Dash, ArcGIS) hentet fra prompt-loggene.
87. Fjern ubenyttet `requirements.txt` i roden og behold `python/requirements.txt` til venv'et.
88. Flet `docs/README.md` og `python/README.md` til et samlet rod-`README.md` og slet de gamle filer.
89. Vurdér tidsplanen for præsentationen ift. 20-minutters slot og foreslå justeringer.
90. Raadgav om Streamlit Cloud-fejlen: manglede plotly, fordi kun rodfilen installeres; anbefalede at oprette requirements.txt i roden (evt. med -r python/requirements.txt) inden redeploy.
91. Flyttede Python-kravene til rodfilen, fjernede python/requirements.txt, opdaterede README-stien og ajourfoerte prompt-loggene.
92. Fjernede stlite-løsningen ved at lade docs/streamlit.html viderestille til Streamlit Cloud og opdaterede forsiden og README til at linke dertil.
93. Loeste TODO 10 ved at linke forsiden til shinyapps.io, bevare Shinylive fallback, tilfoeje deploy-instruks i README og bygge docs/readme.html med automatisk markdown-rendering.
94. Tilfoejet PowerPoint-kort med Office Viewer-link, paafoert note om at opdatere URL og indskrev reglen i agents.md.
95. Erstattede denmark_regions.geojson-referencer med den opdaterede denmark_regions_simple.geojson i værktøj og dokumentation.
96. Skiftede kortapplikationerne tilbage til denmark_regions.geojson og opdaterede helper-scriptet samt Shiny-exporten.
97. Omstrukturerede docs/index.html: PowerPoint-kort først, derefter Streamlit, Dash (screenshot), Shiny, ArcGIS, Power BI (screenshot) og et bonuskort med PowerShell-scripts plus GIF-links.
98. Genetablerede docs/index.html med HTML-entiteter for danske tegn efter skriveadgang blev bekræftet og loggede ændringen.
99. Udvidede forsiden med GitHub-ikon og LinkedIn-kreditering, oprettede dedikerede undersider (præsentation, Dash, Shiny, Power BI, bonus) så alle kort åbner ens i ny fane, og fjernede outline-kortet.
100. Gennemgik GH Pages-linkene, genetablerede praesentation-resurser med videoembed og opdaterede PowerPoint-linket til raw/main, samt bekraeftede at Shiny-undersiden peger paa begge hostingmuligheder.
101. Diagnosticerede ArcGIS Pro clone-fejl som NumPy 2/binary ABI-mismatch (`_ARRAY_API not found`), pinned `numpy<2` i rodfilens requirements og dokumenterede conda-nedgradering i README.
