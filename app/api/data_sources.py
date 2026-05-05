from fastapi import APIRouter, HTTPException, Query

from app.repositories.data_source_repository import DataSourceRepository

router = APIRouter(prefix="/api/v1/data-sources", tags=["data-sources"])


def data_source_to_dict(row):
    return {
        "dataSourceId": row.data_source_id,
        "systemTime": row.system_time.isoformat() if row.system_time else None,
        "name": row.name,
        "description": row.description,
        "provider": row.provider,
        "endpoint": row.endpoint,
        "attributes": row.attributes or {},
        "isDeleted": row.is_deleted,
    }


@router.get("")
def list_data_sources(limit: int = Query(default=20, ge=1, le=100)):
    repository = DataSourceRepository()
    rows = repository.find_all_latest(limit=limit)

    return [data_source_to_dict(row) for row in rows if not row.is_deleted]


@router.get("/{data_source_id}")
def get_data_source(data_source_id: str):
    repository = DataSourceRepository()
    row = repository.find_latest_by_id(data_source_id)

    if row is None or row.is_deleted:
        raise HTTPException(status_code=404, detail="Data source not found")

    return data_source_to_dict(row)
