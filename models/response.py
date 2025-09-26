from typing import Optional, Any
from pydantic import BaseModel


class AnalyzeResponse(BaseModel):
    id: Optional[str]
    raw: Any
    geojson: Any




