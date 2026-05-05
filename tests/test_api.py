from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_assets_endpoint():
    response = client.get("/api/v1/assets")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_asset_detail_endpoint():
    response = client.get("/api/v1/assets/AAPL")

    assert response.status_code == 200

    data = response.json()
    assert data["assetId"] == "AAPL"
    assert data["symbol"] == "AAPL"


def test_data_sources_endpoint():
    response = client.get("/api/v1/data-sources")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_data_source_detail_endpoint():
    response = client.get("/api/v1/data-sources/NASDAQ_CSV")

    assert response.status_code == 200

    data = response.json()
    assert data["dataSourceId"] == "NASDAQ_CSV"


def test_time_series_endpoint():
    response = client.get(
        "/api/v1/data",
        params={
            "assetId": "AAPL",
            "dataSourceId": "NASDAQ_CSV",
            "startBusinessDate": "2024-01-01",
            "endBusinessDate": "2024-01-15",
            "includeAttributes": "true",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["data"]["assetId"] == "AAPL"
    assert data["data"]["dataSourceId"] == "NASDAQ_CSV"
    assert isinstance(data["data"]["records"], list)


def test_analytics_summary_endpoint():
    response = client.get(
        "/api/v1/analytics/summary",
        params={
            "assetId": "AAPL",
            "dataSourceId": "NASDAQ_CSV",
            "year": 2024,
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["assetId"] == "AAPL"
    assert data["dataSourceId"] == "NASDAQ_CSV"
    assert data["count"] > 0


def test_forecast_endpoint():
    response = client.get(
        "/api/v1/analytics/forecast/next-day",
        params={
            "assetId": "AAPL",
            "dataSourceId": "NASDAQ_CSV",
            "year": 2024,
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["assetId"] == "AAPL"
    assert data["dataSourceId"] == "NASDAQ_CSV"
    assert "predictedNextClose" in data
