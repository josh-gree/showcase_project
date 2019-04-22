CREATE TABLE IF NOT EXISTS responsetimes (
    id SERIAL NOT NULL,
    route TEXT,
    time FLOAT,
    request_time TIMESTAMP
)