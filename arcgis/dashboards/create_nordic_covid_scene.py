# -*- coding: utf-8 -*-
"""Create a 3D Nordic COVID-19 deaths scene in ArcGIS Online.

This script uses ArcGIS API for Python together with the OWID dataset located
in `data/owid_covid_global.csv`. It will:

1. Connect to ArcGIS Online (requires `arcgis.gis.GIS("home")` sign-in).
2. Ensure a folder called `dek_2026` exists in the user's content.
3. Build a time-enabled hosted feature layer containing daily COVID-19 deaths
   for the Nordic countries, using Living Atlas country polygons.
4. Publish or refresh a 3D Web Scene that extrudes each country polygon based on
   daily deaths and includes a time slider.

Run:
    python arcgis/dashboards/create_nordic_covid_scene.py
"""

from __future__ import annotations

import json
from datetime import timezone
import math
import tempfile
from pathlib import Path
from typing import Dict, Iterable, List

import pandas as pd
from arcgis.features import FeatureLayer
from arcgis.gis import GIS
from arcgis.geometry import project

WGS84_WKID = 4326
WEB_MERCATOR_WKID = 3857
WGS84_SPATIAL_REFERENCE = {"wkid": WGS84_WKID}
WEB_MERCATOR_SPATIAL_REFERENCE = {"wkid": WEB_MERCATOR_WKID}

NORDIC_COUNTRIES = ["Denmark", "Sweden", "Norway", "Finland", "Iceland"]
FOLDER_NAME = "dek_2026"
FEATURE_LAYER_TITLE = "Nordic COVID-19 Monthly Deaths"
WEB_SCENE_TITLE = "Nordic COVID-19 Monthly Deaths (3D)"
LIVING_ATLAS_COUNTRIES_URL = (
    "https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/"
    "World_Countries_(Generalized)/FeatureServer/0"
)


def _ensure_folder(gis: GIS, folder: str) -> None:
    existing = {f["title"] for f in gis.users.me.folders}
    if folder not in existing:
        gis.content.folders.create(folder)


def _resolve_living_atlas_layer(gis: GIS) -> FeatureLayer:
    try:
        layer = FeatureLayer(LIVING_ATLAS_COUNTRIES_URL, gis=gis)
        _ = layer.properties.name  # touch metadata to validate access
        return layer
    except Exception as exc:  # pragma: no cover - network/resource failure
        raise RuntimeError(
            "Could not access Living Atlas countries layer. "
            "Verify Living Atlas permissions."
        ) from exc


def _detect_name_field(sample_attrs: Dict[str, object]) -> str:
    candidates = ["NAME", "COUNTRY", "CNTRY_NAME", "ADMIN"]
    for field in candidates:
        if field in sample_attrs:
            return field
    raise RuntimeError("Failed to identify a country name field in Living Atlas layer.")


def _load_country_geometries(layer: FeatureLayer) -> Dict[str, Dict[str, object]]:
    field_names = {field["name"] for field in layer.properties.fields}
    name_field = next(
        (candidate for candidate in ["NAME", "COUNTRY", "CNTRY_NAME", "ADMIN"] if candidate in field_names),
        None,
    )
    if not name_field:
        raise RuntimeError("Living Atlas layer does not expose a supported name field.")

    formatted_names = ", ".join(f"'{country}'" for country in NORDIC_COUNTRIES)
    where_clause = f"{name_field} IN ({formatted_names})"
    features = layer.query(
        where=where_clause,
        out_fields=name_field,
        return_geometry=True,
        out_sr=WGS84_SPATIAL_REFERENCE,
        result_record_count=len(NORDIC_COUNTRIES),
        max_allowable_offset=0.05,
        geometry_precision=5,
    )

    geometries: Dict[str, Dict[str, object]] = {}
    for feat in features.features:
        name = feat.attributes[name_field]
        if name in NORDIC_COUNTRIES:
            geometries[name] = feat.as_dict["geometry"]

    missing = set(NORDIC_COUNTRIES) - set(geometries)
    if missing:
        raise RuntimeError(f"Missing geometries for: {', '.join(sorted(missing))}")
    return geometries


def _project_geometries_to_web_mercator(
    geometries: Dict[str, Dict[str, object]], gis: GIS
) -> Dict[str, Dict[str, object]]:
    """Project country polygons to Web Mercator to align with 3D basemap tiling."""
    country_order = list(geometries.keys())
    geometry_payload = []
    for country in country_order:
        geom = dict(geometries[country])
        geom.setdefault("spatialReference", WGS84_SPATIAL_REFERENCE)
        geometry_payload.append(geom)

    projected = project(
        geometries=geometry_payload,
        in_sr=WGS84_SPATIAL_REFERENCE,
        out_sr=WEB_MERCATOR_SPATIAL_REFERENCE,
        gis=gis,
    )

    if not projected or len(projected) != len(country_order):
        raise RuntimeError("Failed to project country geometries to Web Mercator.")

    projected_geometries: Dict[str, Dict[str, object]] = {}
    for country, geom in zip(country_order, projected):
        geom_dict = geom.to_dict() if hasattr(geom, "to_dict") else dict(geom)
        geom_dict.setdefault("spatialReference", WEB_MERCATOR_SPATIAL_REFERENCE)
        projected_geometries[country] = geom_dict

    return projected_geometries


def _lonlat_to_web_mercator(lon: float, lat: float) -> Dict[str, float]:
    """Convert geographic lon/lat to Web Mercator meters for camera positioning."""
    clamped_lat = max(min(lat, 89.9999), -89.9999)
    rad_lat = math.radians(clamped_lat)
    x = math.radians(lon) * 6378137.0
    y = math.log(math.tan((math.pi / 4.0) + (rad_lat / 2.0))) * 6378137.0
    return {"x": x, "y": y}


def _load_covid_data(data_path: Path) -> pd.DataFrame:
    df = pd.read_csv(
        data_path,
        usecols=["location", "date", "new_deaths"],
        parse_dates=["date"],
    )
    df = df[df["location"].isin(NORDIC_COUNTRIES)].copy()
    df["new_deaths"] = df["new_deaths"].fillna(0).clip(lower=0)
    df["date"] = df["date"].dt.to_period("M").dt.to_timestamp("M", "end")
    agg = df.groupby(["location", "date"], as_index=False)["new_deaths"].sum()
    agg["date"] = agg["date"].dt.tz_localize(timezone.utc)
    agg["new_deaths"] = agg["new_deaths"].astype(float)
    return agg.sort_values(["location", "date"])


def _load_population_data(data_path: Path) -> pd.Series:
    df = pd.read_csv(
        data_path,
        usecols=["country", "population_2022"],
    )
    df = df[df["country"].isin(NORDIC_COUNTRIES)].copy()
    missing = set(NORDIC_COUNTRIES) - set(df["country"])
    if missing:
        raise RuntimeError(
            "Population lookup is missing values for: " + ", ".join(sorted(missing))
        )
    df["population_2022"] = df["population_2022"].astype(float)
    return df.set_index("country")["population_2022"]


def _build_feature_records(df: pd.DataFrame, geometries: Dict[str, Dict[str, object]]) -> List[dict]:
    records: List[dict] = []
    for _, row in df.iterrows():
        location = row["location"]
        geometry = dict(geometries[location])
        geometry.setdefault("spatialReference", WEB_MERCATOR_SPATIAL_REFERENCE)
        ts_ms = int(row["date"].timestamp() * 1000)
        records.append(
            {
                "geometry": geometry,
                "attributes": {
                    "country": location,
                    "report_date": ts_ms,
                    "new_deaths": float(row["new_deaths"]),
                    "population_2022": float(row["population_2022"]),
                    "deaths_per_100k": float(row["deaths_per_100k"]),
                },
            }
        )
    return records


def _create_or_update_feature_layer(
    gis: GIS,
    folder: str,
    records: Iterable[dict],
    spatial_reference: Dict[str, object],
    time_extent: Dict[str, int],
) -> FeatureLayer:
    user = gis.users.me
    existing = gis.content.search(
        f'title:"{FEATURE_LAYER_TITLE}" AND owner:{user.username}',
        item_type="Feature Layer",
        max_items=1,
    )

    fields = [
        {"name": "OBJECTID", "type": "esriFieldTypeOID", "alias": "OBJECTID"},
        {"name": "country", "type": "esriFieldTypeString", "alias": "Country", "length": 64},
        {"name": "report_date", "type": "esriFieldTypeDate", "alias": "Report Date"},
        {"name": "new_deaths", "type": "esriFieldTypeDouble", "alias": "Daily deaths"},
        {"name": "population_2022", "type": "esriFieldTypeDouble", "alias": "Population 2022"},
        {"name": "deaths_per_100k", "type": "esriFieldTypeDouble", "alias": "Deaths per 100k"},
    ]

    time_info = {
        "startTimeField": "report_date",
        "timeReference": {"timeZone": "UTC", "respectsDaylightSaving": False},
        "fullTimeExtent": time_extent,
        "timeInterval": 1,
        "timeIntervalUnits": "esriTimeUnitsDays",
        "exportOptions": {"useTime": True},
        "trackIdField": "country",
    }

    feature_set = {
        "geometryType": "esriGeometryPolygon",
        "spatialReference": spatial_reference,
        "features": list(records),
    }

    layer_definition = {
        "name": FEATURE_LAYER_TITLE,
        "geometryType": "esriGeometryPolygon",
        "objectIdField": "OBJECTID",
        "fields": fields,
        "timeInfo": time_info,
    }

    if not existing:
        feature_collection = {"layers": [{"layerDefinition": layer_definition, "featureSet": feature_set}]}
        item_props = {
            "title": FEATURE_LAYER_TITLE,
            "type": "Feature Collection",
            "tags": "covid-19, nordic, deaths, time-enabled",
            "snippet": "Daily COVID-19 deaths for the Nordic countries.",
            "description": (
                "Daily COVID-19 deaths derived from OWID data, joined with Living Atlas country geometries. "
                "Includes 2022 population totals and deaths per 100,000 residents. "
                "Use as a time-enabled layer for 3D visualization."
            ),
        }
        fc_item = gis.content.add(
            item_properties=item_props,
            text=json.dumps(feature_collection),
            folder=folder,
        )
        hosted_item = fc_item.publish()
        fc_item.delete()
        layer = hosted_item.layers[0]
    else:
        hosted_item = existing[0]
        layer = hosted_item.layers[0]
        layer.manager.truncate()

    layer.edit_features(adds=list(feature_set["features"]))
    layer.manager.update_definition({"timeInfo": time_info})
    return layer


def _build_web_scene_json(layer: FeatureLayer, time_extent: Dict[str, int], max_value: float) -> dict:
    height_scale = max(500, max_value * 80)

    operational_layer = {
        "id": "nordic_covid_deaths",
        "layerType": "ArcGISFeatureLayer",
        "url": layer.url,
        "title": FEATURE_LAYER_TITLE,
        "visibility": True,
        "popupInfo": {
            "title": "{country}",
            "fieldInfos": [
                {"fieldName": "report_date", "label": "Date", "isEditable": False, "visible": True},
                {"fieldName": "new_deaths", "label": "Monthly deaths", "isEditable": False, "visible": True},
            ],
            "showAttachments": False,
        },
        "layerDefinition": {
            "drawingInfo": {
                "renderer": {
                    "type": "simple",
                    "symbol": {
                        "type": "polygon-3d",
                        "symbolLayers": [
                            {
                                "type": "extrude",
                                "material": {"color": [214, 48, 49, 220]},
                                "edges": {"type": "solid", "color": [255, 255, 255, 120], "size": 0.6},
                            }
                        ],
                    },
                    "visualVariables": [
                        {
                            "type": "size",
                            "axis": "height",
                            "field": "new_deaths",
                            "legendOptions": {"title": "Monthly deaths"},
                            "stops": [
                                {"value": 0, "size": 0, "label": "0"},
                                {"value": max_value, "size": height_scale, "label": f"{int(max_value)}+"},
                            ],
                        }
                    ],
                }
            },
            "timeInfo": {
                "startTimeField": "report_date",
                "timeReference": {"timeZone": "UTC", "respectsDaylightSaving": False},
                "fullTimeExtent": time_extent,
            },
            "elevationInfo": {"mode": "on-the-ground"},
        },
    }

    application_properties = {
        "viewing": {
            "timeSlider": {
                "isVisible": True,
                "startTime": time_extent["start"],
                "endTime": time_extent["end"],
                "playbackSpeedMultiplier": 1,
                "loop": True,
                "thumbCount": 1,
            }
        }
    }

    camera_xy = _lonlat_to_web_mercator(15.0, 63.5)
    camera_position = {
        "x": camera_xy["x"],
        "y": camera_xy["y"],
        "z": 3500000.0,
        "spatialReference": WEB_MERCATOR_SPATIAL_REFERENCE,
    }

    initial_state = {
        "viewpoint": {
            "camera": {
                "position": camera_position,
                "heading": 20.0,
                "tilt": 48.0,
            }
        },
        "environment": {"lighting": {"displaySunSky": True}},
    }

    return {
        "operationalLayers": [operational_layer],
        "baseMap": {
            "baseMapLayers": [
                {
                    "id": "light_gray_base",
                    "layerType": "ArcGISTiledMapServiceLayer",
                    "url": "https://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer",
                    "visibility": True,
                    "title": "Light Gray Base"
                },
                {
                    "id": "light_gray_reference",
                    "layerType": "ArcGISTiledMapServiceLayer",
                    "url": "https://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Reference/MapServer",
                    "visibility": True,
                    "title": "Light Gray Reference"
                }
            ],
            "title": "Light Gray Canvas",
        },
        "ground": {"layers": []},
        "applicationProperties": application_properties,
        "initialState": initial_state,
        "elevationExaggeration": 1,
        "spatialReference": WEB_MERCATOR_SPATIAL_REFERENCE,
        "version": "1.13",
        "viewingMode": "global",
    }


def _create_or_update_web_scene(gis: GIS, folder: str, scene_json: dict) -> None:
    user = gis.users.me
    existing = gis.content.search(
        f'title:"{WEB_SCENE_TITLE}" AND owner:{user.username}',
        item_type="Web Scene",
        max_items=1,
    )
    item_props = {
        "title": WEB_SCENE_TITLE,
        "type": "Web Scene",
        "tags": "covid-19, nordic, deaths, 3d, time slider",
        "snippet": "3D scene with time-enabled extrusions of Nordic COVID-19 deaths.",
        "description": (
            "A global scene showing daily COVID-19 deaths for the Nordic countries. "
            "Polygon extrusions represent the daily death count, animated with a time slider."
        ),
    }
    scene_data = json.dumps(scene_json)

    if existing:
        scene_item = existing[0]
        try:
            scene_item.update(item_properties=item_props, text=scene_data)
        except TypeError:
            scene_item.update(item_properties=item_props)
            with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tmp:
                tmp.write(scene_data)
                temp_path = tmp.name
            try:
                scene_item.update(data=temp_path)
            finally:
                Path(temp_path).unlink(missing_ok=True)
    else:
        try:
            gis.content.add(item_properties=item_props, text=scene_data, folder=folder)
        except TypeError:
            with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tmp:
                tmp.write(scene_data)
                temp_path = tmp.name
            try:
                gis.content.add(item_properties=item_props, data=temp_path, folder=folder)
            finally:
                Path(temp_path).unlink(missing_ok=True)


def _connect_gis() -> GIS:
    portal_url = None  # Optional: e.g. "https://www.arcgis.com"
    username = None    # Optional: e.g. "my.username"
    password = None    # Optional: password or token

    errors: list[str] = []

    if portal_url and username and password:
        try:
            return GIS(portal_url, username, password)
        except Exception as exc:  # pragma: no cover - logs connection failure
            errors.append(f"Explicit credentials failed: {exc}")

    for profile in ("pro", "home"):
        try:
            return GIS(profile)
        except Exception as exc:  # pragma: no cover - profile may be unavailable
            errors.append(f"GIS('{profile}') failed: {exc}")

    raise RuntimeError(
        "Unable to establish an ArcGIS Online session. "
        "Tried explicit credentials and profiles ('pro', 'home'). "
        + " | ".join(errors)
    )


def main() -> int:
    gis = _connect_gis()
    print(f"Connected to {gis.properties.portalName} as {gis.users.me.username}")
    _ensure_folder(gis, FOLDER_NAME)

    living_atlas_layer = _resolve_living_atlas_layer(gis)
    print("Resolved Living Atlas layer:", living_atlas_layer.url)
    country_geoms = _load_country_geometries(living_atlas_layer)
    print("Loaded geometries for:", ", ".join(sorted(country_geoms)))
    projected_country_geoms = _project_geometries_to_web_mercator(country_geoms, gis)
    print("Projected geometries to Web Mercator.")

    data_path = Path(__file__).resolve().parents[2] / "data" / "owid_covid_global.csv"
    deaths_df = _load_covid_data(data_path)
    print("Loaded deaths rows:", len(deaths_df))
    population_path = Path(__file__).resolve().parents[2] / "data" / "nordic_population_2022.csv"
    population_lookup = _load_population_data(population_path)
    deaths_df["population_2022"] = deaths_df["location"].map(population_lookup)
    if deaths_df["population_2022"].isna().any():
        missing = deaths_df.loc[deaths_df["population_2022"].isna(), "location"].unique()
        raise RuntimeError(
            "Missing population values for: " + ", ".join(sorted(missing))
        )
    deaths_df["deaths_per_100k"] = (
        deaths_df["new_deaths"] / deaths_df["population_2022"].replace({0: pd.NA}) * 100000
    ).fillna(0.0)

    feature_records = _build_feature_records(deaths_df, projected_country_geoms)
    print("Prepared feature records:", len(feature_records))

    start_ts = int(deaths_df["date"].min().timestamp() * 1000)
    end_ts = int(deaths_df["date"].max().timestamp() * 1000)
    time_extent = {"start": start_ts, "end": end_ts}

    feature_layer = _create_or_update_feature_layer(
        gis,
        FOLDER_NAME,
        feature_records,
        spatial_reference=WEB_MERCATOR_SPATIAL_REFERENCE,
        time_extent=time_extent,
    )
    print("Hosted feature layer ready:", feature_layer.url)

    max_value = float(deaths_df["new_deaths"].max() or 1)
    scene_json = _build_web_scene_json(feature_layer, time_extent, max_value)
    _create_or_update_web_scene(gis, FOLDER_NAME, scene_json)

    print("Nordic COVID-19 3D scene updated. Open it in ArcGIS Online to verify extrusion and time slider.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
