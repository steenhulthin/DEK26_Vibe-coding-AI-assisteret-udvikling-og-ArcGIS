# Esri workflow-noter

| Parameter | ArcGIS 3D Web Scene | ArcGIS Dashboards |
| --- | --- | --- |
| Bedst til | Rumlig fortælling, tidsregulator og visuel effekt | Operationelt overblik, KPI'er, selectors og løbende brug |
| Automatisering | God via ArcGIS API for Python og Web Scene JSON | Delvis god: item, webkort og grundlayout kan scriptes, mens fin layoutpolering ofte sker i UI |
| Datagrundlag | Hosted feature layer med tid og geometri | Samme hosted feature layer, gerne suppleret med webkort |
| Deling | ArcGIS Online item, Instant App eller embed | ArcGIS Online item, gruppe/organisation/offentlig deling |
| AI-værdi | Hjælp til dataforberedelse, renderer JSON og scene-konfiguration | Hjælp til dashboardstruktur, item properties og dokumentation |

## Takeaway

ArcGIS API for Python er den vigtigste bro mellem AI-assisteret kodearbejde og et reelt Esri-output. 3D-scenen kan scriptes langt, mens ArcGIS Dashboards typisk er bedst som kombination af scriptet basisopsætning og manuel finjustering i ArcGIS Online.
