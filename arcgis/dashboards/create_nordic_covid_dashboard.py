# -*- coding: utf-8 -*-
"""Create an ArcGIS Dashboards item for the Nordic COVID-19 layer.

Run this after `create_nordic_covid_scene.py`. The script finds the hosted
feature layer created by the scene workflow and creates or updates an ArcGIS
Dashboards item with a map, indicators, serial chart, category selector and
details panel.

Run:
    python arcgis/dashboards/create_nordic_covid_dashboard.py
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from arcgis.gis import GIS

FOLDER_NAME = "dek_2026"
FEATURE_LAYER_TITLE = "Nordic COVID-19 Monthly Deaths"
DASHBOARD_TITLE = "Nordic COVID-19 Dashboard"
WEB_MAP_TITLE = "Nordic COVID-19 Dashboard Map"


def _connect_gis() -> GIS:
    errors: list[str] = []
    for profile in ("pro", "home"):
        try:
            return GIS(profile)
        except Exception as exc:  # pragma: no cover - profile may be unavailable
            errors.append(f"GIS('{profile}') failed: {exc}")

    raise RuntimeError(
        "Unable to establish an ArcGIS Online session. "
        "Tried profiles ('pro', 'home'). " + " | ".join(errors)
    )


def _ensure_folder(gis: GIS, folder: str) -> None:
    existing = {f["title"] for f in gis.users.me.folders}
    if folder not in existing:
        gis.content.folders.create(folder)


def _find_feature_layer(gis: GIS):
    user = gis.users.me
    matches = gis.content.search(
        f'title:"{FEATURE_LAYER_TITLE}" AND owner:{user.username}',
        item_type="Feature Layer",
        max_items=1,
    )
    if not matches:
        raise RuntimeError(
            f'Could not find "{FEATURE_LAYER_TITLE}". '
            "Run create_nordic_covid_scene.py first."
        )
    return matches[0], matches[0].layers[0]


def _create_or_update_web_map(gis: GIS, folder: str, layer_item, layer) -> str:
    user = gis.users.me
    matches = gis.content.search(
        f'title:"{WEB_MAP_TITLE}" AND owner:{user.username}',
        item_type="Web Map",
        max_items=1,
    )
    web_map_json = {
        "operationalLayers": [
            {
                "id": "nordic_covid_deaths",
                "itemId": layer_item.itemid,
                "layerType": "ArcGISFeatureLayer",
                "url": layer.url,
                "title": FEATURE_LAYER_TITLE,
                "visibility": True,
                "popupInfo": {
                    "title": "{country}",
                    "fieldInfos": [
                        {"fieldName": "report_date", "label": "Month", "visible": True},
                        {"fieldName": "new_deaths", "label": "Monthly deaths", "visible": True},
                        {"fieldName": "deaths_per_100k", "label": "Deaths per 100k", "visible": True},
                    ],
                },
                "layerDefinition": {
                    "drawingInfo": {
                        "renderer": {
                            "type": "simple",
                            "symbol": {
                                "type": "esriSFS",
                                "style": "esriSFSSolid",
                                "color": [34, 139, 230, 170],
                                "outline": {"color": [255, 255, 255, 200], "width": 1},
                            },
                            "visualVariables": [
                                {
                                    "type": "colorInfo",
                                    "field": "deaths_per_100k",
                                    "stops": [
                                        {"value": 0, "color": [237, 248, 251, 170]},
                                        {"value": 5, "color": [102, 194, 164, 190]},
                                        {"value": 15, "color": [44, 127, 184, 210]},
                                    ],
                                }
                            ],
                        }
                    }
                },
            }
        ],
        "baseMap": {
            "baseMapLayers": [
                {
                    "id": "gray_base",
                    "layerType": "ArcGISTiledMapServiceLayer",
                    "url": "https://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer",
                    "visibility": True,
                }
            ],
            "title": "Light Gray Canvas",
        },
        "spatialReference": {"wkid": 102100, "latestWkid": 3857},
        "version": "2.29",
    }
    props = {
        "title": WEB_MAP_TITLE,
        "type": "Web Map",
        "tags": "dek-2026, arcgis dashboards, covid-19, nordic",
        "snippet": "Web map used by the DEK 2026 ArcGIS Dashboard example.",
    }
    text = json.dumps(web_map_json)
    if matches:
        item = matches[0]
        item.update(item_properties=props, text=text)
    else:
        item = gis.content.add(item_properties=props, text=text, folder=folder)
    return item.itemid


def _dashboard_json(web_map_id: str, layer_url: str) -> dict:
    layer_ref = {
        "type": "serviceDataset",
        "dataSource": {"type": "featureServiceDataSource", "url": layer_url},
    }
    return {
        "version": 48,
        "authoringApp": "ArcGIS Dashboards",
        "authoringAppVersion": "11.4",
        "header": {
            "title": "Nordic COVID-19 Dashboard",
            "subtitle": "ArcGIS Dashboards example for Dansk Esri Konference 2026",
        },
        "widgets": [
            {
                "id": "map",
                "type": "mapWidget",
                "name": "Map",
                "map": {"itemId": web_map_id},
            },
            {
                "id": "total_deaths",
                "type": "indicatorWidget",
                "name": "Monthly deaths",
                "datasets": [{"id": "main", **layer_ref}],
                "statistic": {"type": "sum", "field": "new_deaths"},
                "valueType": "statistic",
            },
            {
                "id": "rate",
                "type": "indicatorWidget",
                "name": "Deaths per 100k",
                "datasets": [{"id": "main", **layer_ref}],
                "statistic": {"type": "avg", "field": "deaths_per_100k"},
                "valueType": "statistic",
            },
            {
                "id": "trend",
                "type": "serialChartWidget",
                "name": "Monthly trend",
                "datasets": [{"id": "main", **layer_ref}],
                "category": {"field": "report_date", "type": "date"},
                "value": {"field": "new_deaths", "statisticType": "sum"},
            },
            {
                "id": "country_selector",
                "type": "categorySelectorWidget",
                "name": "Country",
                "datasets": [{"id": "main", **layer_ref}],
                "category": {"field": "country"},
            },
            {
                "id": "details",
                "type": "detailsWidget",
                "name": "Details",
                "datasets": [{"id": "main", **layer_ref}],
            },
        ],
        "layout": {
            "type": "rootLayout",
            "children": [
                {"type": "itemLayout", "id": "map", "width": 0.58},
                {
                    "type": "stackLayout",
                    "width": 0.42,
                    "children": [
                        {"type": "itemLayout", "id": "country_selector", "height": 0.12},
                        {"type": "itemLayout", "id": "total_deaths", "height": 0.16},
                        {"type": "itemLayout", "id": "rate", "height": 0.16},
                        {"type": "itemLayout", "id": "trend", "height": 0.36},
                        {"type": "itemLayout", "id": "details", "height": 0.20},
                    ],
                },
            ],
        },
    }


def _create_or_update_dashboard(gis: GIS, folder: str, dashboard_json: dict) -> None:
    user = gis.users.me
    matches = gis.content.search(
        f'title:"{DASHBOARD_TITLE}" AND owner:{user.username}',
        item_type="Dashboard",
        max_items=1,
    )
    props = {
        "title": DASHBOARD_TITLE,
        "type": "Dashboard",
        "tags": "dek-2026, arcgis dashboards, covid-19, nordic",
        "snippet": "ArcGIS Dashboards example for Dansk Esri Konference 2026.",
        "description": (
            "Dashboard assembled through ArcGIS API for Python. It uses the hosted "
            "feature layer produced by create_nordic_covid_scene.py."
        ),
    }
    text = json.dumps(dashboard_json)
    if matches:
        item = matches[0]
        try:
            item.update(item_properties=props, text=text)
        except TypeError:
            with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tmp:
                tmp.write(text)
                temp_path = tmp.name
            try:
                item.update(item_properties=props, data=temp_path)
            finally:
                Path(temp_path).unlink(missing_ok=True)
    else:
        try:
            gis.content.add(item_properties=props, text=text, folder=folder)
        except TypeError:
            with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tmp:
                tmp.write(text)
                temp_path = tmp.name
            try:
                gis.content.add(item_properties=props, data=temp_path, folder=folder)
            finally:
                Path(temp_path).unlink(missing_ok=True)


def main() -> int:
    gis = _connect_gis()
    print(f"Connected to {gis.properties.portalName} as {gis.users.me.username}")
    _ensure_folder(gis, FOLDER_NAME)
    layer_item, layer = _find_feature_layer(gis)
    print("Using hosted feature layer:", layer.url)
    web_map_id = _create_or_update_web_map(gis, FOLDER_NAME, layer_item, layer)
    print("Dashboard web map ready:", web_map_id)
    _create_or_update_dashboard(gis, FOLDER_NAME, _dashboard_json(web_map_id, layer.url))
    print("ArcGIS Dashboard item created or updated. Open it in ArcGIS Online to fine-tune layout and selectors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
