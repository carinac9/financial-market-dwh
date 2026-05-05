from datetime import datetime, timezone

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


def main():
    session = get_session()
    system_time = datetime.now(timezone.utc)

    seed_assets(session, system_time)
    seed_data_sources(session, system_time)


if __name__ == "__main__":
    main()
