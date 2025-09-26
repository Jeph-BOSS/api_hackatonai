from fastapi import APIRouter, UploadFile, File, HTTPException, Body
from typing import Optional

from models.response import AnalyzeResponse
from utils.image_utils import read_image_bytes_from_upload, ensure_bytes_from_base64
from services.gemini_service import analyze_image_with_gemini
from utils.format_utils import parse_gemini_to_geojson


router = APIRouter(prefix="", tags=["analyze"])


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_endpoint(
    file: Optional[UploadFile] = File(default=None),
    image_base64: Optional[str] = Body(default=None),
):
    try:
        if file is None and not image_base64:
            raise HTTPException(status_code=400, detail="Aucun fichier ni base64 fourni")

        if file is not None:
            image_bytes = await read_image_bytes_from_upload(file)
        else:
            image_bytes = ensure_bytes_from_base64(image_base64)

        gemini_raw = await analyze_image_with_gemini(image_bytes)
        geojson = parse_gemini_to_geojson(gemini_raw)
        return AnalyzeResponse(id=None, raw=gemini_raw, geojson=geojson)
    except HTTPException:
        raise
    except RuntimeError as exc:
        # Gestion spécifique des erreurs de rate limiting Gemini
        if "Limite de taux dépassée" in str(exc):
            raise HTTPException(status_code=429, detail="Service temporairement surchargé. Veuillez réessayer dans quelques minutes.")
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))




