from typing import List, Optional, Union, Any
from pydantic import BaseModel, Field, field_validator
from typing_extensions import Literal

Coordinates = List[List[List[float]]]

class Geometry(BaseModel):
    type: str
    coordinates: Any
    
    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        allowed = {"Point", "LineString", "Polygon", "MultiPolygon", "MultiLineString", "MultiPoint"}
        if v not in allowed:
            raise ValueError("Type de géométrie non supporté")
        return v

class Feature(BaseModel):
    type: Literal["Feature"] = "Feature"
    geometry: Geometry
    properties: Optional[dict] = Field(default_factory=dict)

class FeatureCollection(BaseModel):
    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: List[Feature]
