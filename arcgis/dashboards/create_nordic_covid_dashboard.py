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
import uuid

from arcgis.gis import GIS

FOLDER_NAME = "dek_2026"
FEATURE_LAYER_TITLE = "Nordic COVID-19 Monthly Deaths"
DASHBOARD_TITLE = "Nordic COVID-19 Dashboard"
WEB_MAP_TITLE = "Nordic COVID-19 Dashboard Map"
WEB_MAP_LAYER_ID = "nordic_covid_deaths"


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


def _update_item_json(item, props: dict, text: str) -> None:
    item.update(item_properties={**props, "text": text})


def _add_item_json(gis: GIS, props: dict, text: str, folder: str):
    return gis.content.add(item_properties={**props, "text": text}, folder=folder)


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
                "id": WEB_MAP_LAYER_ID,
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
        "text": "",
        "verticalAlignment": "middle",
        "showTopCaption": True,
        "showBottomCaption": True,
    }


def _no_value_state() -> dict:
    return {
        "verticalAlignment": "middle",
        "showTopCaption": True,
        "showBottomCaption": True,
    }


def _feature_data_source(layer_item, layer_id: int = 0) -> dict:
    return {
        "type": "layerDataSource",
        "itemId": layer_item.itemid,
        "layerId": layer_id,
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
        "returnDistinctValues": False,
        "allowSourceDownload": False,
        "allowSummaryDownload": False,
    }


def _statistic_field_name(statistic: str, field: str) -> str:
    return f"{statistic}_{field}".upper()


def _indicator_widget(name: str, field: str, statistic: str, layer_item) -> dict:
    widget_id = _new_id()
    statistic_field = _statistic_field_name(statistic, field)
    return {
        "id": widget_id,
        "type": "indicatorWidget",
        "name": name,
        "showLastUpdate": False,
        "noDataState": _no_data_state(),
        "noFilterState": _no_data_state(),
        "noValueState": _no_value_state(),
        "datasets": [
            _service_dataset(
                layer_item,
                [
                    {
                        "onStatisticField": field,
                        "statisticType": statistic,
                        "outStatisticFieldName": statistic_field,
                    }
                ],
            )
        ],
        "defaultSettings": {
            "topSection": {
                "fontSize": 20,
                "textInfo": {"text": name, "fillColor": "#474747"},
            },
            "middleSection": {
                "fontSize": 40,
                "textInfo": {"text": "{calculated/value}", "fillColor": "#367f68"},
            },
            "bottomSection": {"fontSize": 20, "textInfo": {}},
        },
        "comparison": "none",
        "valueType": "statistic",
        "valueFormat": {
            "name": "value",
            "prefix": False,
            "style": "decimal",
            "useGrouping": True,
            "minimumFractionDigits": 0,
            "maximumFractionDigits": 1,
            "valuePrefix": "",
            "valueSuffix": "",
        },
        "percentageFormat": {
            "name": "percentage",
            "prefix": False,
            "style": "percent",
            "useGrouping": True,
            "minimumFractionDigits": 0,
            "maximumFractionDigits": 2,
            "valuePrefix": "",
            "valueSuffix": "",
        },
        "ratioFormat": {
            "name": "ratio",
            "prefix": False,
            "style": "decimal",
            "useGrouping": True,
            "minimumFractionDigits": 0,
            "maximumFractionDigits": 2,
            "valuePrefix": "",
            "valueSuffix": "",
        },
    }


def _rich_text_widget() -> dict:
    return {
        "id": _new_id(),
        "type": "richTextWidget",
        "name": "Details",
        "showLastUpdate": False,
        "noDataState": _no_data_state(),
        "noFilterState": _no_data_state(),
        "text": (
            "<h3>Details</h3>"
            "<p>Use the map pop-ups to inspect country and month values.</p>"
        ),
    }


def _serial_chart_widget(layer_item) -> dict:
    statistic_field = "SUM_NEW_DEATHS"
    dataset = _service_dataset(
        layer_item,
        [
            {
                "onStatisticField": "new_deaths",
                "statisticType": "sum",
                "outStatisticFieldName": statistic_field,
            }
        ],
    )
    dataset["groupByFields"] = ["report_date"]
    dataset["orderByFields"] = ["report_date asc"]
    return {
        "id": _new_id(),
        "type": "serialChartWidget",
        "name": "Monthly trend",
        "topCaption": "<p style=\"text-align:center\"><strong>Monthly trend</strong></p>\n",
        "showLastUpdate": False,
        "noDataState": _no_data_state(),
        "noFilterState": _no_data_state(),
        "datasets": [dataset],
        "actionMode": "monoSelection",
        "categoryType": "groupByValues",
        "valueFormat": {
            "name": "value",
            "prefix": False,
            "style": "decimal",
            "useGrouping": True,
            "minimumFractionDigits": 0,
            "maximumFractionDigits": 1,
            "valuePrefix": "",
            "valueSuffix": "",
        },
        "labelFormat": {
            "name": "label",
            "prefix": False,
            "style": "decimal",
            "useGrouping": True,
            "minimumFractionDigits": 0,
            "maximumFractionDigits": 1,
            "valuePrefix": "",
            "valueSuffix": "",
        },
        "category": {
            "labelOverrides": [],
            "nullLabel": "null",
            "blankLabel": "blank",
        },
        "parseDates": True,
        "minPeriod": "MM",
        "categoryAxisLabelsBehavior": "hide",
        "chartConfig": {
            "version": "24.4.0",
            "type": "chart",
            "orderOptions": {},
            "colorMatch": False,
            "axes": [
                {
                    "type": "chartAxis",
                    "visible": True,
                    "title": {
                        "type": "chartText",
                        "visible": True,
                        "content": {
                            "type": "esriTS",
                            "angle": 0,
                            "font": {
                                "family": "inherit",
                                "style": "normal",
                                "weight": "bold",
                            },
                            "text": "Month",
                        },
                    },
                    "valueFormat": {"type": "category", "characterLimit": 11},
                    "lineSymbol": _chart_line_symbol(0.5),
                    "labels": _chart_text(True),
                    "grid": _chart_line_symbol(0.15),
                    "guides": [],
                    "scrollbar": {"visible": True, "width": 15, "gripSize": 22},
                },
                {
                    "type": "chartAxis",
                    "visible": True,
                    "title": {
                        "type": "chartText",
                        "visible": True,
                        "content": {
                            "type": "esriTS",
                            "angle": 270,
                            "font": {
                                "family": "inherit",
                                "style": "normal",
                                "weight": "bold",
                            },
                            "text": "Monthly deaths",
                        },
                    },
                    "valueFormat": {
                        "type": "number",
                        "intlOptions": {
                            "style": "decimal",
                            "notation": "standard",
                            "minimumFractionDigits": 0,
                            "maximumFractionDigits": 1,
                        },
                    },
                    "lineSymbol": _chart_line_symbol(0.5),
                    "labels": _chart_text(True),
                    "grid": _chart_line_symbol(0.15),
                    "guides": [],
                    "integerOnlyValues": False,
                    "isLogarithmic": False,
                    "buffer": True,
                },
            ],
            "series": [
                {
                    "type": "barSeries",
                    "id": "value",
                    "name": "Monthly deaths",
                    "x": "report_date",
                    "dataLabels": _chart_text(False),
                    "dataTooltipVisible": True,
                    "dataTooltipReverseColor": True,
                    "y": statistic_field,
                    "fillSymbol": {
                        "type": "esriSFS",
                        "style": "esriSFSSolid",
                        "color": [44, 127, 184, 255],
                        "outline": {
                            "type": "esriSLS",
                            "style": "esriSLSSolid",
                            "color": [44, 127, 184, 255],
                            "width": 1,
                        },
                    },
                }
            ],
            "legend": {
                "type": "chartLegend",
                "visible": False,
                "body": _chart_text(True)["content"],
                "position": "bottom",
            },
            "horizontalAxisLabelsBehavior": "hide",
            "verticalAxisLabelsBehavior": "hide",
            "rotated": False,
            "cursorCrosshair": {"type": "cursorCrosshair"},
            "stackedType": "sideBySide",
        },
    }


def _chart_text(visible: bool) -> dict:
    return {
        "type": "chartText",
        "visible": visible,
        "content": {
            "type": "esriTS",
            "angle": 0,
            "font": {
                "family": "inherit",
                "style": "normal",
                "weight": "normal",
            },
        },
    }


def _chart_line_symbol(alpha: float) -> dict:
    return {
        "type": "esriSLS",
        "style": "esriSLSSolid",
        "color": [202, 202, 202, 255 * alpha],
        "width": 1,
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


def _number_prefix_overrides() -> list[dict]:
    keys = [
        ("yotta", "Y", False),
        ("zeta", "Z", False),
        ("exa", "E", False),
        ("peta", "P", False),
        ("tera", "T", False),
        ("giga", "G", False),
        ("mega", "M", False),
        ("kilo", "k", False),
        ("base", "", True),
        ("deci", "d", False),
        ("centi", "c", False),
        ("milli", "m", False),
        ("micro", "µ", False),
        ("nano", "n", False),
    ]
    return [
        {"key": key, "symbol": symbol, "enabled": enabled}
        for key, symbol, enabled in keys
    ]


def _date_filter_targets(map_widget: dict, data_widgets: list[dict]) -> list[dict]:
    targets = [
        {
            "targetId": f"{map_widget['id']}#{WEB_MAP_LAYER_ID}",
            "by": "whereClause",
            "requiresSelection": False,
            "fieldMap": [{"sourceName": "filterField", "targetName": "report_date"}],
        }
    ]
    targets.extend(
        {
            "targetId": f"{widget['id']}#main",
            "by": "whereClause",
            "requiresSelection": False,
            "fieldMap": [{"sourceName": "filterField", "targetName": "report_date"}],
        }
        for widget in data_widgets
    )
    return targets


def _date_selector(map_widget: dict, data_widgets: list[dict]) -> dict:
    return {
        "id": _new_id(),
        "name": "Date selector",
        "showLastUpdate": False,
        "noDataState": _no_data_state(),
        "noFilterState": _no_data_state(),
        "events": [
            {
                "type": "selectionChanged",
                "actions": [
                    {
                        "type": "filter",
                        "targets": _date_filter_targets(map_widget, data_widgets),
                    }
                ],
            }
        ],
        "label": "Report date",
        "caption": "Report date",
        "type": "dateSelectorWidget",
        "optionType": "datePicker",
        "datePickerOption": {
            "type": "datePicker",
            "selectionType": "range",
            "operator": "between",
        },
        "presentationMode": "accordion",
    }


def _sidebar(selectors: list[dict]) -> dict:
    return {
        "selectors": selectors,
        "type": "sidebar",
        "topCaption": "<h3 style=\"text-align:center\"><strong>Filters</strong></h3>\n",
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
        "mapTools": [{"type": "legendTool"}, {"type": "mapContentsTool"}],
        "showMeasureTool": False,
        "showNavigation": True,
        "showPanRotate": False,
        "showLocate": False,
        "showCompass": False,
        "showPopup": True,
        "scalebarStyle": "none",
        "editingEnabled": False,
        "selectionColor": "#ff00ff",
        "highlightColor": "#ff00ff",
        "trackedFeatureColor": "#0000ff",
        "trackedFeatureRadius": 60,
        "selectTool": {
            "type": "selectTool",
            "clickToSelect": False,
            "advanceSketchTools": [],
        },
    }
    total_deaths = _indicator_widget("Monthly deaths", "new_deaths", "sum", layer_item)
    rate = _indicator_widget("Deaths per 100k", "deaths_per_100k", "avg", layer_item)
    trend = _serial_chart_widget(layer_item)
    details = _rich_text_widget()
    widgets = [map_widget, total_deaths, rate, trend, details]
    data_widgets = [total_deaths, rate, trend]
    side_column = _stack_layout(
        [
            _item_layout(total_deaths, height=0.18),
            _item_layout(rate, height=0.18),
            _item_layout(trend, height=0.42),
            _item_layout(details, height=0.22),
        ],
        orientation="row",
        width=0.42,
    )
    return {
        "version": "4.34.0",
        "authoringApp": "ArcGIS Dashboards",
        "authoringAppVersion": "4.34.0+python",
        "maxPaginationRecords": 50000,
        "maxChartRecords": 10000,
        "timeZone": "system",
        "theme": {"id": "user", "type": "resource"},
        "numberPrefixOverrides": _number_prefix_overrides(),
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
                    orientation="col",
                ),
            },
            "settings": {
                "allowElementResizing": False,
                "allowElementExpansion": True,
                "allowReset": False,
            },
            "sidebar": _sidebar([_date_selector(map_widget, data_widgets)]),
        },
        "elementMappings": {},
    }


def _create_or_update_dashboard(gis: GIS, folder: str, dashboard_json: dict):
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
        return item
    else:
        return _add_item_json(gis, props, text, folder)


def _upgrade_dashboard_item(gis: GIS, dashboard_item) -> None:
    try:
        from arcgis.apps.dashboards import DashboardManager
    except ImportError:
        return

    try:
        DashboardManager(item=dashboard_item, gis=gis).upgrade()
        print("Dashboard schema upgraded with arcgis.apps.dashboards.DashboardManager.")
    except Exception as exc:  # pragma: no cover - depends on ArcGIS API version
        print("DashboardManager upgrade skipped:", exc)


def main() -> int:
    gis = _connect_gis()
    print(f"Connected to {gis.properties.portalName} as {gis.users.me.username}")
    _ensure_folder(gis, FOLDER_NAME)
    layer_item, layer = _find_feature_layer(gis)
    print("Using hosted feature layer:", layer.url)
    web_map_id = _create_or_update_web_map(gis, FOLDER_NAME, layer_item, layer)
    print("Dashboard web map ready:", web_map_id)
    dashboard_item = _create_or_update_dashboard(
        gis,
        FOLDER_NAME,
        _dashboard_json(web_map_id, layer_item),
    )
    _upgrade_dashboard_item(gis, dashboard_item)
    print("ArcGIS Dashboard item created or updated. Open it in ArcGIS Online to fine-tune layout and selectors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
