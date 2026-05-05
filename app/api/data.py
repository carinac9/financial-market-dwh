from datetime import date

from fastapi import APIRouter, Query

from app.repositories.time_series_repository import TimeSeriesRepository

router = APIRouter(prefix="/api/v1/data", tags=["time-series-data"])


def record_to_dict(row):
    return {
        "businessDate": str(row.business_date),
        "systemTime": row.system_time.isoformat() if row.system_time else None,
        "valuesDouble": row.values_double or {},
        "valuesInt": row.values_int or {},
        "valuesText": row.values_text or {},
        "provenance": row.provenance or {},
    }


@router.get("")
def get_time_series_data(
    asset_id: str = Query(alias="assetId"),
    data_source_id: str = Query(alias="dataSourceId"),
    start_business_date: date = Query(alias="startBusinessDate"),
    end_business_date: date = Query(alias="endBusinessDate"),
    include_attributes: bool = Query(default=False, alias="includeAttributes"),
):
    repository = TimeSeriesRepository()

    rows = repository.find_latest_records(
        asset_id=asset_id,
        data_source_id=data_source_id,
        start_business_date=start_business_date,
        end_business_date=end_business_date,
    )

    response = {
        "data": {
            "assetId": asset_id,
            "dataSourceId": data_source_id,
            "records": [record_to_dict(row) for row in rows],
        }
    }

    if include_attributes:
        attributes = set()

        for row in rows:
            attributes.update((row.values_double or {}).keys())
            attributes.update((row.values_int or {}).keys())
            attributes.update((row.values_text or {}).keys())

        response["attributes"] = sorted(attributes)

    return response
