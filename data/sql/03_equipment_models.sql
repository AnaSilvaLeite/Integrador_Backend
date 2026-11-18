
USE integrador;

INSERT INTO equipment_model (name, description)
SELECT
    'ESP8266',
    'Microcontrolador utilizado nos pontos de monitoramento ambiental'
WHERE NOT EXISTS (
    SELECT 1
    FROM equipment_model
    WHERE name = 'ESP8266'
);
