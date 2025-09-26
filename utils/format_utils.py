from typing import Any, Dict
from models.geojson import FeatureCollection, Feature, Geometry


def parse_gemini_to_geojson(gemini_raw: Dict[str, Any]) -> Dict[str, Any]:
    # Le service Gemini renvoie soit {"parsed": {...}} soit {"text": "..."}
    import json

    payload: Dict[str, Any] = {}
    if "parsed" in gemini_raw and isinstance(gemini_raw["parsed"], dict):
        payload = gemini_raw["parsed"]
    elif "text" in gemini_raw and isinstance(gemini_raw["text"], str):
        try:
            payload = json.loads(gemini_raw["text"])
        except Exception:
            payload = {}

    # Normaliser en FeatureCollection
    if not payload:
        payload = {"type": "FeatureCollection", "features": []}

    if payload.get("type") != "FeatureCollection":
        # supposer que payload est une liste de features ou une seule feature/geometry
        features = []
        if isinstance(payload, list):
            for item in payload:
                feat = _normalize_to_feature(item)
                if feat:
                    features.append(feat)
        else:
            feat = _normalize_to_feature(payload)
            if feat:
                features.append(feat)
        payload = {"type": "FeatureCollection", "features": features}

    # Validation Pydantic (soulève si invalide)
    fc = FeatureCollection(**payload)
    return fc.dict()


def _normalize_to_feature(obj: Any) -> Dict[str, Any]:
    if not isinstance(obj, dict):
        return {}
    if obj.get("type") == "Feature":
        return obj
    if "geometry" in obj:
        return {"type": "Feature", "geometry": obj["geometry"], "properties": obj.get("properties", {})}
    # peut-être un geometry direct
    if "type" in obj and "coordinates" in obj:
        return {"type": "Feature", "geometry": {"type": obj["type"], "coordinates": obj["coordinates"]}, "properties": {}}
    return {}




