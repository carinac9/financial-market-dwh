from fastapi import APIRouter, HTTPException, Query

from app.repositories.asset_repository import AssetRepository

router = APIRouter(prefix="/api/v1/assets", tags=["assets"])


def asset_to_dict(row):
    return {
        "assetId": row.asset_id,
        "systemTime": row.system_time.isoformat() if row.system_time else None,
        "symbol": row.symbol,
        "assetType": row.asset_type,
        "region": row.region,
        "name": row.name,
        "description": row.description,
        "attributes": row.attributes or {},
        "isDeleted": row.is_deleted,
    }


@router.get("")
def list_assets(limit: int = Query(default=20, ge=1, le=100)):
    repository = AssetRepository()
    rows = repository.find_all_latest(limit=limit)
    return [asset_to_dict(row) for row in rows if not row.is_deleted]


@router.get("/{asset_id}")
def get_asset(asset_id: str):
    repository = AssetRepository()
    row = repository.find_latest_by_id(asset_id)

    if row is None or row.is_deleted:
        raise HTTPException(status_code=404, detail="Asset not found")

    return asset_to_dict(row)
