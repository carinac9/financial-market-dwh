from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.repositories.asset_repository import AssetRepository
from app.repositories.data_source_repository import DataSourceRepository

router = APIRouter(prefix="/ui", tags=["ui"])

templates = Jinja2Templates(directory="app/templates")


def asset_to_dict(row):
    return {
        "assetId": row.asset_id,
        "symbol": row.symbol,
        "assetType": row.asset_type,
        "region": row.region,
        "name": row.name,
        "description": row.description,
        "attributes": row.attributes or {},
        "systemTime": row.system_time.isoformat() if row.system_time else None,
    }


def data_source_to_dict(row):
    return {
        "dataSourceId": row.data_source_id,
        "name": row.name,
        "provider": row.provider,
        "endpoint": row.endpoint,
        "description": row.description,
        "attributes": row.attributes or {},
    }


@router.get("")
def dashboard(request: Request):
    asset_repository = AssetRepository()
    source_repository = DataSourceRepository()

    assets = [
        asset_to_dict(row)
        for row in asset_repository.find_all_latest(limit=50)
        if not row.is_deleted
    ]

    data_sources = [
        data_source_to_dict(row)
        for row in source_repository.find_all_latest(limit=50)
        if not row.is_deleted
    ]

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "assets": assets,
            "data_sources": data_sources,
        },
    )


@router.get("/assets/{asset_id}")
def asset_detail(request: Request, asset_id: str):
    asset_repository = AssetRepository()
    asset = asset_repository.find_latest_by_id(asset_id)

    return templates.TemplateResponse(
        request,
        "asset_detail.html",
        {
            "asset": asset_to_dict(asset) if asset else None,
        },
    )
