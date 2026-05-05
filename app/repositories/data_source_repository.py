from app.core.cassandra import get_session


class DataSourceRepository:
    def __init__(self):
        self.session = get_session()

    def find_all_latest(self, limit: int = 20):
        query = """
        SELECT data_source_id, system_time, name, description, provider,
               endpoint, attributes, is_deleted
        FROM data_sources
        LIMIT %s
        """

        rows = self.session.execute(query, (limit,))
        latest_by_source = {}

        for row in rows:
            if row.data_source_id not in latest_by_source:
                latest_by_source[row.data_source_id] = row

        return list(latest_by_source.values())

    def find_latest_by_id(self, data_source_id: str):
        query = """
        SELECT data_source_id, system_time, name, description, provider,
               endpoint, attributes, is_deleted
        FROM data_sources
        WHERE data_source_id = %s
        LIMIT 1
        """

        return self.session.execute(query, (data_source_id,)).one()
