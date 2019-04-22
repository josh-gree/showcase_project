CREATE VIEW last_minute AS
SELECT 
    *
FROM 
    responsetimes
WHERE
    "request_time" >= NOW() - INTERVAL '1 minutes';