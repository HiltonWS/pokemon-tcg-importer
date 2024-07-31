CREATE TABLE IF NOT EXISTS 'set' (
    id TEXT PRIMARY KEY,
    name TEXT,
    series TEXT
);
CREATE TABLE IF NOT EXISTS card (
    id TEXT PRIMARY KEY,
    number TEXT,
    name TEXT,
    image TEXT,
    rarity TEXT,
    eu_price DECIMAL,
    set_id TEXT,
    FOREIGN KEY (set_id) REFERENCES sets(set_id)
);