from fastapi import APIRouter, HTTPException, Depends

from services.storage_service import StorageService, get_storage


router = APIRouter(prefix="", tags=["map"])


@router.get("/map/{record_id}")
def get_map(record_id: str, storage: StorageService = Depends(get_storage)):
    result = storage.get_result(record_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Non trouvé")
    return result["geojson"]




