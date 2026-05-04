CREATE KEYSPACE IF NOT EXISTS financial_dwh
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

CREATE TABLE IF NOT EXISTS financial_dwh.assets (
  asset_id text,
  system_time timestamp,
  symbol text,
  asset_type text,
  region text,
  name text,
  description text,
  attributes map<text, text>,
  is_deleted boolean,
  PRIMARY KEY (asset_id, system_time)
) WITH CLUSTERING ORDER BY (system_time DESC);

CREATE TABLE IF NOT EXISTS financial_dwh.data_sources (
  data_source_id text,
  system_time timestamp,
  name text,
  description text,
  provider text,
  endpoint text,
  attributes map<text, text>,
  is_deleted boolean,
  PRIMARY KEY (data_source_id, system_time)
) WITH CLUSTERING ORDER BY (system_time DESC);

CREATE TABLE IF NOT EXISTS financial_dwh.time_series_data (
  asset_id text,
  data_source_id text,
  business_year int,
  business_date date,
  system_time timestamp,
  values_double map<text, double>,
  values_int map<text, int>,
  values_text map<text, text>,
  provenance map<text, text>,
  is_deleted boolean,
  PRIMARY KEY (
    (asset_id, data_source_id, business_year),
    business_date,
    system_time
  )
) WITH CLUSTERING ORDER BY (
  business_date DESC,
  system_time DESC
);
