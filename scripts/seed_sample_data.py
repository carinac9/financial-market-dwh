from datetime import date, datetime, timezone

from app.core.cassandra import get_session


def seed_assets(session, system_time):
    assets = [
        {
            "asset_id": "AAPL",
            "symbol": "AAPL",
            "asset_type": "stock",
            "region": "US",
            "name": "Apple Inc.",
            "description": "Technology company listed on NASDAQ",
            "attributes": {
                "sector": "Technology",
                "currency": "USD",
            },
        },
        {
            "asset_id": "MSFT",
            "symbol": "MSFT",
            "asset_type": "stock",
            "region": "US",
            "name": "Microsoft Corporation",
            "description": "Technology company listed on NASDAQ",
            "attributes": {
                "sector": "Technology",
                "currency": "USD",
            },
        },
        {
            "asset_id": "BTCUSD",
            "symbol": "BTC/USD",
            "asset_type": "crypto",
            "region": "Global",
            "name": "Bitcoin / US Dollar",
            "description": "Bitcoin price quoted in US dollars",
            "attributes": {
                "base": "BTC",
                "quote": "USD",
            },
        },
    ]

    query = """
    INSERT INTO assets (
        asset_id, system_time, symbol, asset_type, region,
        name, description, attributes, is_deleted
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for asset in assets:
        session.execute(
            query,
            (
                asset["asset_id"],
                system_time,
                asset["symbol"],
                asset["asset_type"],
                asset["region"],
                asset["name"],
                asset["description"],
                asset["attributes"],
                False,
            ),
        )

    print("Seeded sample assets.")


def seed_data_sources(session, system_time):
    data_sources = [
        {
            "data_source_id": "NASDAQ_SAMPLE",
            "name": "Nasdaq Sample Market Data",
            "description": "Sample stock market data provider used for project testing",
            "provider": "Nasdaq Data Link",
            "endpoint": "sample/local",
            "attributes": {
                "supported_indicators": "Open,High,Low,Close,Volume",
                "data_type": "historical_prices",
            },
        },
        {
            "data_source_id": "COINBASE_SAMPLE",
            "name": "Coinbase Sample Crypto Data",
            "description": "Sample crypto market data provider used for project testing",
            "provider": "Coinbase",
            "endpoint": "sample/local",
            "attributes": {
                "supported_indicators": "Open,High,Low,Close,Volume",
                "data_type": "historical_crypto_prices",
            },
        },
    ]

    query = """
    INSERT INTO data_sources (
        data_source_id, system_time, name, description, provider,
        endpoint, attributes, is_deleted
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    for source in data_sources:
        session.execute(
            query,
            (
                source["data_source_id"],
                system_time,
                source["name"],
                source["description"],
                source["provider"],
                source["endpoint"],
                source["attributes"],
                False,
            ),
        )

    print("Seeded sample data sources.")


def seed_time_series_data(session, system_time):
    records = [
        {
            "asset_id": "AAPL",
            "data_source_id": "NASDAQ_SAMPLE",
            "business_date": date(2024, 1, 2),
            "values_double": {
                "Open": 185.64,
                "High": 188.44,
                "Low": 183.89,
                "Close": 187.15,
            },
            "values_int": {
                "Volume": 82488700,
            },
            "values_text": {},
        },
        {
            "asset_id": "AAPL",
            "data_source_id": "NASDAQ_SAMPLE",
            "business_date": date(2024, 1, 3),
            "values_double": {
                "Open": 186.00,
                "High": 187.05,
                "Low": 183.20,
                "Close": 184.25,
            },
            "values_int": {
                "Volume": 58414500,
            },
            "values_text": {},
        },
        {
            "asset_id": "AAPL",
            "data_source_id": "NASDAQ_SAMPLE",
            "business_date": date(2024, 1, 4),
            "values_double": {
                "Open": 184.30,
                "High": 185.88,
                "Low": 183.43,
                "Close": 181.91,
            },
            "values_int": {
                "Volume": 71983600,
            },
            "values_text": {},
        },
        {
            "asset_id": "MSFT",
            "data_source_id": "NASDAQ_SAMPLE",
            "business_date": date(2024, 1, 2),
            "values_double": {
                "Open": 373.86,
                "High": 375.90,
                "Low": 366.77,
                "Close": 370.87,
            },
            "values_int": {
                "Volume": 25258600,
            },
            "values_text": {},
        },
        {
            "asset_id": "MSFT",
            "data_source_id": "NASDAQ_SAMPLE",
            "business_date": date(2024, 1, 3),
            "values_double": {
                "Open": 369.01,
                "High": 373.26,
                "Low": 368.51,
                "Close": 370.60,
            },
            "values_int": {
                "Volume": 23083500,
            },
            "values_text": {},
        },
        {
            "asset_id": "BTCUSD",
            "data_source_id": "COINBASE_SAMPLE",
            "business_date": date(2024, 1, 2),
            "values_double": {
                "Open": 44187.00,
                "High": 45900.00,
                "Low": 44100.00,
                "Close": 44950.00,
            },
            "values_int": {
                "Volume": 31500,
            },
            "values_text": {
                "Market": "Crypto",
            },
        },
        {
            "asset_id": "BTCUSD",
            "data_source_id": "COINBASE_SAMPLE",
            "business_date": date(2024, 1, 3),
            "values_double": {
                "Open": 44950.00,
                "High": 45500.00,
                "Low": 40800.00,
                "Close": 42870.00,
            },
            "values_int": {
                "Volume": 38200,
            },
            "values_text": {
                "Market": "Crypto",
            },
        },
    ]

    query = """
    INSERT INTO time_series_data (
        asset_id, data_source_id, business_year, business_date, system_time,
        values_double, values_int, values_text, provenance, is_deleted
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for record in records:
        provenance = {
            "provider": record["data_source_id"],
            "ingestion_type": "sample_seed",
            "source": "local_sample_data",
        }

        session.execute(
            query,
            (
                record["asset_id"],
                record["data_source_id"],
                record["business_date"].year,
                record["business_date"],
                system_time,
                record["values_double"],
                record["values_int"],
                record["values_text"],
                provenance,
                False,
            ),
        )

    print("Seeded sample time-series data.")


def main():
    session = get_session()
    system_time = datetime.now(timezone.utc)

    seed_assets(session, system_time)
    seed_data_sources(session, system_time)
    seed_time_series_data(session, system_time)


if __name__ == "__main__":
    main()
