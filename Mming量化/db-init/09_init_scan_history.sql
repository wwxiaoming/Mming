CREATE TABLE IF NOT EXISTS scan_history (
    id              VARCHAR(128) PRIMARY KEY,
    strategy_name   VARCHAR(128) NOT NULL,
    market          VARCHAR(10)  NOT NULL,
    period          VARCHAR(10)  NOT NULL,
    start_date      VARCHAR(10)  NOT NULL,
    end_date        VARCHAR(10)  NOT NULL,
    total_symbols   INT          NOT NULL DEFAULT 0,
    processed       INT          NOT NULL DEFAULT 0,
    failed          INT          NOT NULL DEFAULT 0,
    strategy_script TEXT,
    scan_summary    JSONB,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

ALTER TABLE scan_history ADD COLUMN IF NOT EXISTS strategy_script TEXT;
ALTER TABLE scan_history ADD COLUMN IF NOT EXISTS filters_json JSONB;

CREATE INDEX IF NOT EXISTS idx_sh_created ON scan_history(created_at DESC);
