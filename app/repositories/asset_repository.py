from app.core.cassandra import get_session


class AssetRepository:
    def __init__(self):
        self.session = get_session()

    def find_all_latest(self, limit: int = 20):
        query = """
        SELECT asset_id, system_time, symbol, asset_type, region, name, description, attributes, is_deleted
        FROM assets
        LIMIT %s
        """
        rows = self.session.execute(query, (limit,))

        latest_by_asset = {}

        for row in rows:
            if row.asset_id not in latest_by_asset:
                latest_by_asset[row.asset_id] = row

        return list(latest_by_asset.values())

    def find_latest_by_id(self, asset_id: str):
        query = """
        SELECT asset_id, system_time, symbol, asset_type, region, name, description, attributes, is_deleted
        FROM assets
        WHERE asset_id = %s
        LIMIT 1
        """
        return self.session.execute(query, (asset_id,)).one()
