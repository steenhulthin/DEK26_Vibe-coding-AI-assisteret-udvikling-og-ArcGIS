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
import uuid
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


def _write_temp_json(text: str) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tmp:
        tmp.write(text)
        return tmp.name


def _update_item_json(item, props: dict, text: str) -> None:
    try:
        item.update(item_properties=props, text=text)
    except TypeError:
        temp_path = _write_temp_json(text)
        try:
            item.update(item_properties=props, data=temp_path)
        finally:
            Path(temp_path).unlink(missing_ok=True)


def _add_item_json(gis: GIS, props: dict, text: str, folder: str):
    try:
        return gis.content.add(item_properties=props, text=text, folder=folder)
    except TypeError:
        temp_path = _write_temp_json(text)
        try:
            return gis.content.add(item_properties=props, data=temp_path, folder=folder)
        finally:
            Path(temp_path).unlink(missing_ok=True)


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
        _update_item_json(item, props, text)
    else:
        item = _add_item_json(gis, props, text, folder)
    return item.itemid


def _new_id() -> str:
    return str(uuid.uuid4())


def _no_data_state() -> dict:
    return {
        "verticalAlignment": "middle",
        "showCaption": True,
        "showDescription": True,
    }


def _feature_data_source(layer_item, layer_id: int = 0) -> dict:
    return {
        "type": "featureServiceDataSource",
        "itemId": layer_item.itemid,
        "layerId": layer_id,
        "table": True,
    }


def _service_dataset(layer_item, statistic_definitions: list[dict] | None = None) -> dict:
    return {
        "type": "serviceDataset",
        "name": "main",
        "dataSource": _feature_data_source(layer_item),
        "outFields": ["*"],
        "groupByFields": [],
        "orderByFields": [],
        "statisticDefinitions": statistic_definitions or [],
        "querySpatialRelationship": "esriSpatialRelIntersects",
        "returnGeometry": False,
        "clientSideStatistics": False,
    }


def _indicator_widget(name: str, field: str, statistic: str, layer_item) -> dict:
    widget_id = _new_id()
    return {
        "id": widget_id,
        "type": "indicatorWidget",
        "name": name,
        "caption": name,
        "description": "",
        "showLastUpdate": True,
        "noDataState": _no_data_state(),
        "noFilterState": _no_data_state(),
        "datasets": [
            _service_dataset(
                layer_item,
                [
                    {
                        "onStatisticField": field,
                        "outStatisticFieldName": "value",
                        "statisticType": statistic,
                    }
                ],
            )
        ],
        "defaultSettings": {
            "topSection": {"fontSize": 80, "textInfo": {"text": name}},
            "middleSection": {"fontSize": 160, "textInfo": {"text": "{value}"}},
            "bottomSection": {"fontSize": 80, "textInfo": {}},
        },
        "comparison": "none",
        "valueField": field,
        "referenceField": "",
        "valueConversion": {"factor": 1, "offset": 0},
        "referenceConversion": {"factor": 1, "offset": 0},
        "valueType": "statistic",
        "valueFormat": {
            "name": "value",
            "style": "decimal",
            "useGrouping": True,
            "maximumFractionDigits": 1,
            "prefix": False,
        },
        "percentageFormat": {
            "name": "percentage",
            "style": "percent",
            "useGrouping": True,
            "maximumFractionDigits": 2,
            "prefix": False,
        },
        "ratioFormat": {
            "name": "ratio",
            "style": "decimal",
            "useGrouping": True,
            "maximumFractionDigits": 2,
            "prefix": False,
        },
    }


def _details_widget(layer_item) -> dict:
    return {
        "id": _new_id(),
        "type": "detailsWidget",
        "name": "Details",
        "caption": "Details",
        "description": "",
        "showLastUpdate": True,
        "noDataState": _no_data_state(),
        "noFilterState": _no_data_state(),
        "showTitle": True,
        "showContents": True,
        "showMedia": True,
        "showAttachments": True,
        "datasets": [
            {
                **_service_dataset(layer_item),
                "maxFeatures": 50,
            }
        ],
    }


def _serial_chart_widget(layer_item) -> dict:
    dataset = _service_dataset(
        layer_item,
        [
            {
                "onStatisticField": "new_deaths",
                "outStatisticFieldName": "value",
                "statisticType": "sum",
            }
        ],
    )
    dataset["groupByFields"] = ["report_date"]
    dataset["orderByFields"] = ["report_date asc"]
    return {
        "id": _new_id(),
        "type": "serialChartWidget",
        "name": "Monthly trend",
        "caption": "Monthly trend",
        "description": "",
        "showLastUpdate": True,
        "noDataState": _no_data_state(),
        "noFilterState": _no_data_state(),
        "datasets": [dataset],
        "categoryType": "groupByValues",
        "category": {
            "fieldName": "report_date",
            "labelOverrides": [],
            "byCategoryColors": False,
            "labelsPlacement": "default",
            "labelRotation": 0,
            "nullLabel": "Null",
            "blankLabel": "Blank",
            "defaultColor": "#d6d6d6",
            "nullColor": "#d6d6d6",
            "blankColor": "#d6d6d6",
        },
        "categoryAxis": {
            "title": "Month",
            "titleRotation": 0,
            "titleFontSize": 12,
            "fontSize": 12,
            "gridThickness": 1,
            "gridAlpha": 0.15,
            "gridColor": "#ffffff",
            "axisThickness": 1,
            "axisAlpha": 0.5,
            "axisColor": "#000000",
            "labelsEnabled": True,
            "gridPosition": "start",
            "parseDates": True,
            "minPeriod": "MM",
        },
        "valueAxis": {
            "title": "Monthly deaths",
            "titleRotation": 270,
            "titleFontSize": 12,
            "fontSize": 12,
            "gridThickness": 1,
            "gridAlpha": 0.15,
            "gridColor": "#ffffff",
            "axisThickness": 1,
            "axisAlpha": 0.5,
            "axisColor": "#000000",
            "labelsEnabled": True,
            "stackType": "none",
        },
        "graphs": [
            {
                "type": "column",
                "valueField": "value",
                "title": "Monthly deaths",
                "lineColorField": "_lineColor_",
                "fillColorsField": "_fillColor_",
                "fillAlphas": 1,
                "lineAlpha": 1,
                "lineThickness": 1,
                "bullet": "none",
                "showBalloon": True,
            }
        ],
        "legend": {
            "enabled": False,
            "position": "bottom",
            "markerSize": 15,
            "markerType": "circle",
            "align": "center",
            "labelWidth": 100,
            "valueWidth": 0,
        },
        "splitBy": {"defaultColor": "#d6d6d6", "seriesProperties": []},
        "chartScrollbar": {"enabled": False},
        "commonGraphProperties": {"type": "column"},
        "guides": [],
        "events": [],
        "selectionMode": "multi",
        "rotate": False,
        "fontSize": 11,
        "color": "#474747",
        "valueFormat": {
            "name": "value",
            "style": "decimal",
            "useGrouping": True,
            "maximumFractionDigits": 1,
            "prefix": True,
        },
        "labelFormat": {
            "name": "label",
            "style": "decimal",
            "useGrouping": True,
            "maximumFractionDigits": 1,
            "prefix": True,
        },
    }


def _item_layout(widget: dict, width: float = 1, height: float = 1) -> dict:
    return {
        "type": "itemLayoutElement",
        "id": widget["id"],
        "width": width,
        "height": height,
    }


def _stack_layout(
    elements: list[dict],
    orientation: str,
    width: float = 1,
    height: float = 1,
) -> dict:
    return {
        "id": _new_id(),
        "type": "stackLayoutElement",
        "orientation": orientation,
        "width": width,
        "height": height,
        "elements": elements,
    }


def _dashboard_json(web_map_id: str, layer_item) -> dict:
    map_widget = {
        "id": _new_id(),
        "type": "mapWidget",
        "name": "Map",
        "showLastUpdate": False,
        "noDataState": _no_data_state(),
        "noFilterState": _no_data_state(),
        "flashRepeats": 3,
        "itemId": web_map_id,
        "mapTools": [],
        "showNavigation": True,
        "showLocate": False,
        "showCompass": False,
        "showPopup": True,
        "scalebarStyle": "none",
        "groupSelect": "none",
    }
    total_deaths = _indicator_widget("Monthly deaths", "new_deaths", "sum", layer_item)
    rate = _indicator_widget("Deaths per 100k", "deaths_per_100k", "avg", layer_item)
    trend = _serial_chart_widget(layer_item)
    details = _details_widget(layer_item)
    widgets = [map_widget, total_deaths, rate, trend, details]
    side_column = _stack_layout(
        [
            _item_layout(total_deaths, height=0.18),
            _item_layout(rate, height=0.18),
            _item_layout(trend, height=0.42),
            _item_layout(details, height=0.22),
        ],
        orientation="col",
        width=0.42,
    )
    return {
        "version": 55,
        "authoringApp": "ArcGIS Dashboards",
        "authoringAppVersion": "4.27.0+python",
        "maxPaginationRecords": 50000,
        "mapOverrides": {
            "highlightColor": "#ff00ff",
            "trackedFeatureColor": "#0000ff",
            "trackedFeatureRadius": 60,
        },
        "theme": "light",
        "themeOverrides": {},
        "numberPrefixOverrides": [],
        "desktopView": {
            "type": "desktop",
            "widgets": widgets,
            "layout": {
                "type": "dockingLayout",
                "rootElement": _stack_layout(
                    [
                        _item_layout(map_widget, width=0.58),
                        side_column,
                    ],
                    orientation="row",
                ),
            },
            "settings": {
                "allowElementResizing": False,
                "allowElementExpansion": True,
                "allowReset": False,
            },
        },
        "elementMappings": {},
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
        _update_item_json(item, props, text)
    else:
        _add_item_json(gis, props, text, folder)


def main() -> int:
    gis = _connect_gis()
    print(f"Connected to {gis.properties.portalName} as {gis.users.me.username}")
    _ensure_folder(gis, FOLDER_NAME)
    layer_item, layer = _find_feature_layer(gis)
    print("Using hosted feature layer:", layer.url)
    web_map_id = _create_or_update_web_map(gis, FOLDER_NAME, layer_item, layer)
    print("Dashboard web map ready:", web_map_id)
    _create_or_update_dashboard(gis, FOLDER_NAME, _dashboard_json(web_map_id, layer_item))
    print("ArcGIS Dashboard item created or updated. Open it in ArcGIS Online to fine-tune layout and selectors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
