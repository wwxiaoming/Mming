-- =============================================================================
-- K-line storage — 7 hypertables, one per period.
--
-- Each row stores a single OHLCV candle for one (market, symbol, ts) tuple.
-- The capacity cap (max 2500 rows per (market, symbol) per table) is enforced
-- in application code (CleanupOldKlinesUseCase), not by a SQL trigger, because
-- we want the cleanup to also run an explicit VACUUM to release chunk space.
--
-- This file is idempotent — the in-app SchemaMigrator re-applies it on every
-- boot, so do NOT add any destructive statements here. Use CREATE ... IF NOT
-- EXISTS only.
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS timescaledb;
SET timezone = 'America/New_York';

-- ─── Helper: a DO block defines all 7 tables in a loop to avoid copy-paste ────
-- Each table:
--   ts        TIMESTAMPTZ NOT NULL  (the time bucket of this candle)
--   symbol    VARCHAR(20) NOT NULL
--   market    VARCHAR(10) NOT NULL  -- 'CN' / 'HK' / 'US' / 'CRYPTO'
--   open/high/low/close DOUBLE PRECISION
--   volume    BIGINT
-- with a unique index on (market, symbol, ts DESC) for fast incremental queries.

DO $$
DECLARE
    p TEXT;
    tbl TEXT;
    periods TEXT[] := ARRAY['1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'];
BEGIN
    FOREACH p IN ARRAY periods LOOP
        tbl := 'kline_' || p;
        EXECUTE format($f$
            CREATE TABLE IF NOT EXISTS %I (
                ts          TIMESTAMPTZ      NOT NULL,
                symbol      VARCHAR(20)      NOT NULL,
                market      VARCHAR(10)      NOT NULL,
                open        DOUBLE PRECISION,
                high        DOUBLE PRECISION,
                low         DOUBLE PRECISION,
                close       DOUBLE PRECISION,
                volume      BIGINT
            )
        $f$, tbl);

        -- Convert to a TimescaleDB hypertable partitioned on ts.
        -- if_not_exists handles re-runs of this script.
        EXECUTE format($f$
            SELECT create_hypertable(%L, 'ts', if_not_exists => TRUE)
        $f$, tbl);

        -- Composite unique index — speeds up the dominant query pattern:
        --   "give me rows for THIS symbol+market between dates, newest first"
        EXECUTE format($f$
            CREATE UNIQUE INDEX IF NOT EXISTS %I
                ON %I (market, symbol, ts DESC)
        $f$, 'idx_' || p || '_market_symbol_ts', tbl);
    END LOOP;
END $$;
