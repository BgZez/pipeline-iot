-- View 1: estatísticas de temperatura por local do sensor (interno/externo).
-- Obs.: no dataset todas as leituras vêm do mesmo room_id, então a
-- comparação útil entre "dispositivos" é In (dentro) x Out (fora).
CREATE OR REPLACE VIEW avg_temp_por_local AS
SELECT
    location,
    ROUND(AVG(temperature)::numeric, 2) AS avg_temp,
    MIN(temperature)                    AS min_temp,
    MAX(temperature)                    AS max_temp,
    COUNT(*)                            AS total_leituras
FROM temperature_readings
GROUP BY location;

-- View 2: volume de leituras e temperatura média por hora do dia.
CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT
    CAST(EXTRACT(HOUR FROM noted_date) AS INT) AS hora,
    COUNT(*)                                   AS contagem,
    ROUND(AVG(temperature)::numeric, 2)        AS avg_temp
FROM temperature_readings
GROUP BY 1
ORDER BY 1;

-- View 3: temperaturas máxima, mínima e média por dia.
CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT
    CAST(noted_date AS DATE)            AS data,
    MAX(temperature)                    AS temp_max,
    MIN(temperature)                    AS temp_min,
    ROUND(AVG(temperature)::numeric, 2) AS temp_avg
FROM temperature_readings
GROUP BY 1
ORDER BY 1;
