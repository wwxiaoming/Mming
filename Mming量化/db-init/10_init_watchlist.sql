CREATE TABLE IF NOT EXISTS watchlist_groups (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(64)  NOT NULL,
    sort_order  INT          NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS watchlist_items (
    group_id    INT          NOT NULL REFERENCES watchlist_groups(id) ON DELETE CASCADE,
    symbol      VARCHAR(20)  NOT NULL,
    market      VARCHAR(10)  NOT NULL,
    name        VARCHAR(128),
    added_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    PRIMARY KEY (group_id, symbol, market)
);

CREATE INDEX IF NOT EXISTS idx_wl_items_group ON watchlist_items(group_id);
