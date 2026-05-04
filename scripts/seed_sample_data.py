from datetime import datetime, timezone

from app.core.cassandra import get_session


def main():
    session = get_session()
    now = datetime.now(timezone.utc)

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
                "currency": "USD"
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
                "currency": "USD"
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
                "quote": "USD"
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
                now,
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


if __name__ == "__main__":
    main()
