-- 盘面监控（Market Monitor）
-- monitor_watch_items: 用户配置的"标的+周期+策略组合"
-- monitor_signals:     定时回测扫到的"最新 K 线触发的开/平仓信号"
-- monitor_user_state:  单用户单机 App，用单行存"上次查看信号的时间戳"，配合查询计算未读数

CREATE TABLE IF NOT EXISTS monitor_watch_items (
    id            SERIAL PRIMARY KEY,
    symbol        VARCHAR(20)  NOT NULL,
    market        VARCHAR(10)  NOT NULL,
    period        VARCHAR(10)  NOT NULL,
    strategy_ids  JSONB        NOT NULL DEFAULT '[]'::jsonb,
    sort_order    INT          NOT NULL DEFAULT 0,
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    UNIQUE (symbol, market, period)
);

CREATE INDEX IF NOT EXISTS idx_mwi_sort ON monitor_watch_items(sort_order, id);

CREATE TABLE IF NOT EXISTS monitor_signals (
    id               BIGSERIAL PRIMARY KEY,
    watch_item_id    INT          NOT NULL REFERENCES monitor_watch_items(id) ON DELETE CASCADE,
    symbol           VARCHAR(20)  NOT NULL,
    market           VARCHAR(10)  NOT NULL,
    period           VARCHAR(10)  NOT NULL,
    signal_type      VARCHAR(16)  NOT NULL,
    signal_bar_date  VARCHAR(20)  NOT NULL,
    signal_price     NUMERIC(18,8) NOT NULL,
    strategy_id      VARCHAR(128),
    strategy_name    VARCHAR(128),
    detected_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    UNIQUE (watch_item_id, signal_bar_date, signal_type, strategy_id)
);

CREATE INDEX IF NOT EXISTS idx_ms_recent ON monitor_signals(detected_at DESC);
CREATE INDEX IF NOT EXISTS idx_ms_item ON monitor_signals(watch_item_id, detected_at DESC);

CREATE TABLE IF NOT EXISTS monitor_user_state (
    id                    INT          PRIMARY KEY DEFAULT 1 CHECK (id = 1),
    signals_last_seen_at  TIMESTAMPTZ  NOT NULL DEFAULT '1970-01-01'::timestamptz,
    webhook_url           VARCHAR(1024)
);

INSERT INTO monitor_user_state (id) VALUES (1) ON CONFLICT (id) DO NOTHING;

-- v1.1: add webhook_url for external notifications
ALTER TABLE monitor_user_state ADD COLUMN IF NOT EXISTS webhook_url VARCHAR(1024);

-- v1.2: per-item daily/weekly/monthly trigger offset. Positive integer =
-- minutes BEFORE market close to fire the scan (1-10), so A-share users
-- can act in the closing auction same-day. 0 (default) preserves the
-- legacy 5-minute post-close window — old rows aren't impacted.
ALTER TABLE monitor_watch_items
  ADD COLUMN IF NOT EXISTS daily_trigger_minutes_before_close SMALLINT NOT NULL DEFAULT 0;
