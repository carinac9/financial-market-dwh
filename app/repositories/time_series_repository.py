from datetime import date

from app.core.cassandra import get_session


class TimeSeriesRepository:
    def __init__(self):
        self.session = get_session()

    def find_latest_records(
        self,
        asset_id: str,
        data_source_id: str,
        start_business_date: date,
        end_business_date: date,
    ):
        records = []

        start_year = start_business_date.year
        end_year = end_business_date.year

        query = """
        SELECT asset_id, data_source_id, business_year, business_date, system_time,
               values_double, values_int, values_text, provenance, is_deleted
        FROM time_series_data
        WHERE asset_id = %s
          AND data_source_id = %s
          AND business_year = %s
          AND business_date >= %s
          AND business_date < %s
        """

        for year in range(start_year, end_year + 1):
            rows = self.session.execute(
                query,
                (
                    asset_id,
                    data_source_id,
                    year,
                    start_business_date,
                    end_business_date,
                ),
            )

            latest_by_business_date = {}

            for row in rows:
                existing = latest_by_business_date.get(row.business_date)

                if existing is None or row.system_time > existing.system_time:
                    latest_by_business_date[row.business_date] = row

            records.extend(
                row
                for row in latest_by_business_date.values()
                if not row.is_deleted
            )

        return sorted(records, key=lambda row: row.business_date, reverse=True)
