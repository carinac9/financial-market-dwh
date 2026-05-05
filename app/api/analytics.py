from datetime import date
from statistics import mean

from fastapi import APIRouter, HTTPException, Query

from app.repositories.time_series_repository import TimeSeriesRepository

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])


def extract_close_points(rows):
    close_points = []

    for row in rows:
        values = row.values_double or {}

        if "Close" in values:
            close_points.append(
                {
                    "businessDate": str(row.business_date),
                    "close": float(values["Close"]),
                }
            )

    return sorted(close_points, key=lambda item: item["businessDate"])


@router.get("/summary")
def get_summary(
    asset_id: str = Query(alias="assetId"),
    data_source_id: str = Query(alias="dataSourceId"),
    year: int = Query(ge=1900, le=2100),
):
    repository = TimeSeriesRepository()

    rows = repository.find_latest_records(
        asset_id=asset_id,
        data_source_id=data_source_id,
        start_business_date=date(year, 1, 1),
        end_business_date=date(year + 1, 1, 1),
    )

    close_points = extract_close_points(rows)

    if not close_points:
        raise HTTPException(
            status_code=404,
            detail="No close price data found for the requested asset/source/year",
        )

    close_values = [point["close"] for point in close_points]
    first_close = close_values[0]
    last_close = close_values[-1]

    percentage_change = None
    if first_close != 0:
        percentage_change = ((last_close - first_close) / first_close) * 100

    return {
        "assetId": asset_id,
        "dataSourceId": data_source_id,
        "year": year,
        "metric": "Close",
        "count": len(close_values),
        "minClose": min(close_values),
        "maxClose": max(close_values),
        "avgClose": sum(close_values) / len(close_values),
        "firstClose": first_close,
        "lastClose": last_close,
        "percentageChange": percentage_change,
        "points": close_points,
    }


@router.get("/forecast/next-day")
def forecast_next_day(
    asset_id: str = Query(alias="assetId"),
    data_source_id: str = Query(alias="dataSourceId"),
    year: int = Query(ge=1900, le=2100),
):
    repository = TimeSeriesRepository()

    rows = repository.find_latest_records(
        asset_id=asset_id,
        data_source_id=data_source_id,
        start_business_date=date(year, 1, 1),
        end_business_date=date(year + 1, 1, 1),
    )

    close_points = extract_close_points(rows)

    if len(close_points) < 2:
        raise HTTPException(
            status_code=400,
            detail="At least two close price points are required for forecasting",
        )

    close_values = [point["close"] for point in close_points]

    daily_changes = [
        close_values[index] - close_values[index - 1]
        for index in range(1, len(close_values))
    ]

    average_change = mean(daily_changes)
    predicted_close = close_values[-1] + average_change

    return {
        "assetId": asset_id,
        "dataSourceId": data_source_id,
        "year": year,
        "method": "average_daily_close_change",
        "lastKnownDate": close_points[-1]["businessDate"],
        "lastKnownClose": close_values[-1],
        "averageDailyChange": average_change,
        "predictedNextClose": predicted_close,
        "pointsUsed": close_points,
    }
