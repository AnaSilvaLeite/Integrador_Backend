
USE integrador;

INSERT INTO microcontroller (
    mac_address,
    latitude,
    longitude,
    observation,
    status,
    registration_date,
    equipment_model_id,
    environment_id
)
SELECT
    'AA:BB:CC:00:00:01',
    -23.5505200,
    -46.6333080,
    'Instalado no ponto de monitoramento 01',
    'ACTIVE',
    UTC_TIMESTAMP(),
    (SELECT id FROM equipment_model WHERE name = 'ESP8266'),
    (SELECT id FROM environment WHERE point = 'PONTO01')
WHERE NOT EXISTS (
    SELECT 1 FROM microcontroller
    WHERE mac_address = 'AA:BB:CC:00:00:01'
);

INSERT INTO microcontroller (
    mac_address, latitude, longitude, observation, status,
    registration_date, equipment_model_id, environment_id
)
SELECT
    'AA:BB:CC:00:00:02',
    -23.5515200,
    -46.6343080,
    'Instalado no ponto de monitoramento 02',
    'ACTIVE',
    UTC_TIMESTAMP(),
    (SELECT id FROM equipment_model WHERE name = 'ESP8266'),
    (SELECT id FROM environment WHERE point = 'PONTO02')
WHERE NOT EXISTS (
    SELECT 1 FROM microcontroller
    WHERE mac_address = 'AA:BB:CC:00:00:02'
);

INSERT INTO microcontroller (
    mac_address, latitude, longitude, observation, status,
    registration_date, equipment_model_id, environment_id
)
SELECT
    'AA:BB:CC:00:00:03',
    -23.5525200,
    -46.6353080,
    'Instalado no ponto de monitoramento 03',
    'ACTIVE',
    UTC_TIMESTAMP(),
    (SELECT id FROM equipment_model WHERE name = 'ESP8266'),
    (SELECT id FROM environment WHERE point = 'PONTO03')
WHERE NOT EXISTS (
    SELECT 1 FROM microcontroller
    WHERE mac_address = 'AA:BB:CC:00:00:03'
);

INSERT INTO microcontroller (
    mac_address, latitude, longitude, observation, status,
    registration_date, equipment_model_id, environment_id
)
SELECT
    'AA:BB:CC:00:00:04',
    -23.5535200,
    -46.6363080,
    'Instalado no ponto de monitoramento 04',
    'ACTIVE',
    UTC_TIMESTAMP(),
    (SELECT id FROM equipment_model WHERE name = 'ESP8266'),
    (SELECT id FROM environment WHERE point = 'PONTO04')
WHERE NOT EXISTS (
    SELECT 1 FROM microcontroller
    WHERE mac_address = 'AA:BB:CC:00:00:04'
);

INSERT INTO microcontroller (
    mac_address, latitude, longitude, observation, status,
    registration_date, equipment_model_id, environment_id
)
SELECT
    'AA:BB:CC:00:00:05',
    -23.5545200,
    -46.6373080,
    'Instalado no ponto de monitoramento 05',
    'ACTIVE',
    UTC_TIMESTAMP(),
    (SELECT id FROM equipment_model WHERE name = 'ESP8266'),
    (SELECT id FROM environment WHERE point = 'PONTO05')
WHERE NOT EXISTS (
    SELECT 1 FROM microcontroller
    WHERE mac_address = 'AA:BB:CC:00:00:05'
);
