CREATE TABLE IF NOT EXISTS backtest_history (
    id              VARCHAR(128) PRIMARY KEY,
    strategy_id     VARCHAR(64)  NOT NULL,
    strategy_name   VARCHAR(128) NOT NULL,
    symbol          VARCHAR(20)  NOT NULL,
    market          VARCHAR(10)  NOT NULL,
    period          VARCHAR(10)  NOT NULL,
    start_date      VARCHAR(10)  NOT NULL,
    end_date        VARCHAR(10)  NOT NULL,
    leverage        NUMERIC(10,2) NOT NULL DEFAULT 1,
    commission_rate NUMERIC(10,4) NOT NULL DEFAULT 0,
    strategy_script TEXT,
    backtest_result JSONB        NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

ALTER TABLE backtest_history ADD COLUMN IF NOT EXISTS strategy_script TEXT;

CREATE INDEX IF NOT EXISTS idx_bh_updated ON backtest_history(updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_bh_strategy ON backtest_history(strategy_id);
