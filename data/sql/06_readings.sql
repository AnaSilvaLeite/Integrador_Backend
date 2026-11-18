
USE integrador;

INSERT INTO reading (
    registration_date,
    sensor_id,
    measured_value
)
SELECT
    dados.registration_date,
    dados.sensor_id,
    dados.measured_value
FROM (
    SELECT
        s.id AS sensor_id,

        DATE_ADD(
            TIMESTAMP(
                '2026-10-01',
                MAKETIME(8 + (2 * horarios.step), mc.reading_minute, 0)
            ),
            INTERVAL 3 HOUR
        ) AS registration_date,

        (
            CASE s.function
                WHEN 'temperature' THEN 22.10
                WHEN 'humidity' THEN 60.10
                WHEN 'luminosity' THEN 350.10
                WHEN 'counter' THEN 1.10
            END
            + mc.offset_value
            + (horarios.step * 0.50)
        ) AS measured_value

    FROM (
        SELECT 'AA:BB:CC:00:00:01' AS mac_address, 6 AS reading_minute, 0.00 AS offset_value
        UNION ALL
        SELECT 'AA:BB:CC:00:00:02', 9, 0.10
        UNION ALL
        SELECT 'AA:BB:CC:00:00:03', 12, 0.20
        UNION ALL
        SELECT 'AA:BB:CC:00:00:04', 15, 0.30
        UNION ALL
        SELECT 'AA:BB:CC:00:00:05', 18, 0.40
    ) AS mc

    INNER JOIN microcontroller m
        ON m.mac_address = mc.mac_address

    INNER JOIN sensor s
        ON s.microcontroller_id = m.id

    CROSS JOIN (
        SELECT 0 AS step
        UNION ALL SELECT 1
        UNION ALL SELECT 2
        UNION ALL SELECT 3
        UNION ALL SELECT 4
    ) AS horarios

) AS dados

WHERE NOT EXISTS (
    SELECT 1
    FROM reading r
    WHERE r.sensor_id = dados.sensor_id
      AND r.registration_date = dados.registration_date
      AND r.measured_value = dados.measured_value
);
