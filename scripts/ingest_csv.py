import csv
from datetime import datetime, timezone
from pathlib import Path

from app.core.cassandra import get_session


CSV_PATH = Path("data/sample_market_data.csv")


def insert_asset(session, row, system_time):
    query = """
    INSERT INTO assets (
        asset_id, system_time, symbol, asset_type, region,
        name, description, attributes, is_deleted
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    attributes = {
        "source": "csv_ingestion",
        "currency": "USD",
    }

    session.execute(
        query,
        (
            row["asset_id"],
            system_time,
            row["symbol"],
            row["asset_type"],
            row["region"],
            row["asset_name"],
            row["asset_description"],
            attributes,
            False,
        ),
    )


def insert_data_source(session, row, system_time):
    query = """
    INSERT INTO data_sources (
        data_source_id, system_time, name, description, provider,
        endpoint, attributes, is_deleted
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    attributes = {
        "supported_indicators": "Open,High,Low,Close,Volume",
        "ingestion_format": "csv",
    }

    session.execute(
        query,
        (
            row["data_source_id"],
            system_time,
            row["source_name"],
            "CSV-ingested sample market data provider",
            row["provider"],
            row["endpoint"],
            attributes,
            False,
        ),
    )


def insert_time_series_record(session, row, system_time):
    business_date = datetime.strptime(row["business_date"], "%Y-%m-%d").date()

    query = """
    INSERT INTO time_series_data (
        asset_id, data_source_id, business_year, business_date, system_time,
        values_double, values_int, values_text, provenance, is_deleted
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values_double = {
        "Open": float(row["open"]),
        "High": float(row["high"]),
        "Low": float(row["low"]),
        "Close": float(row["close"]),
    }

    values_int = {
        "Volume": int(row["volume"]),
    }

    values_text = {
        "ingestionFormat": "csv",
    }

    provenance = {
        "provider": row["provider"],
        "data_source_id": row["data_source_id"],
        "endpoint": row["endpoint"],
        "file": str(CSV_PATH),
        "ingested_by": "scripts/ingest_csv.py",
    }

    session.execute(
        query,
        (
            row["asset_id"],
            row["data_source_id"],
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


def main():
    session = get_session()
    system_time = datetime.now(timezone.utc)

    inserted_rows = 0
    seen_assets = set()
    seen_sources = set()

    with CSV_PATH.open(mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            asset_id = row["asset_id"]
            data_source_id = row["data_source_id"]

            if asset_id not in seen_assets:
                insert_asset(session, row, system_time)
                seen_assets.add(asset_id)

            if data_source_id not in seen_sources:
                insert_data_source(session, row, system_time)
                seen_sources.add(data_source_id)

            insert_time_series_record(session, row, system_time)
            inserted_rows += 1

    print("CSV ingestion completed.")
    print(f"Assets inserted/updated: {len(seen_assets)}")
    print(f"Data sources inserted/updated: {len(seen_sources)}")
    print(f"Time-series records inserted: {inserted_rows}")


if __name__ == "__main__":
    main()
