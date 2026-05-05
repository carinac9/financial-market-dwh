from datetime import date, datetime, timezone

from app.core.cassandra import get_session


def main():
    session = get_session()

    asset_id = "AAPL"
    data_source_id = "NASDAQ_CSV"
    business_date = date(2024, 1, 9)
    system_time = datetime.now(timezone.utc)

    query = """
    INSERT INTO time_series_data (
        asset_id, data_source_id, business_year, business_date, system_time,
        values_double, values_int, values_text, provenance, is_deleted
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values_double = {
        "Open": 183.92,
        "High": 185.15,
        "Low": 182.73,
        "Close": 186.50,
    }

    values_int = {
        "Volume": 42841800,
    }

    values_text = {
        "correction": "true",
        "correctionReason": "Corrected close price after data quality review",
    }

    provenance = {
        "provider": "Nasdaq Data Link",
        "data_source_id": data_source_id,
        "endpoint": "csv/sample",
        "correction_type": "manual_demo_correction",
        "ingested_by": "scripts/demo_temporal_versioning.py",
    }

    session.execute(
        query,
        (
            asset_id,
            data_source_id,
            business_date.year,
            business_date,
            system_time,
            values_double,
            values_int,
            values_text,
            provenance,
            False,
        ),
    )

    print("Inserted corrected temporal version.")
    print(f"Asset: {asset_id}")
    print(f"Source: {data_source_id}")
    print(f"Business date: {business_date}")
    print(f"New system time: {system_time.isoformat()}")
    print("Corrected Close price: 186.50")


if __name__ == "__main__":
    main()
