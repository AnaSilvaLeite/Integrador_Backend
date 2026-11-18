
USE integrador;

-- Microcontrolador 01
INSERT INTO sensor (function, model, unit_measureament, status, microcontroller_id)
SELECT 'temperature', 'Sensor de temperatura', '°C', 'ACTIVE', m.id
FROM microcontroller m
WHERE m.mac_address = 'AA:BB:CC:00:00:01'
AND NOT EXISTS (
    SELECT 1 FROM sensor s
    WHERE s.microcontroller_id = m.id
    AND s.function = 'temperature'
);

INSERT INTO sensor (function, model, unit_measureament, status, microcontroller_id)
SELECT 'humidity', 'Sensor de umidade', '%', 'ACTIVE', m.id
FROM microcontroller m
WHERE m.mac_address = 'AA:BB:CC:00:00:01'
AND NOT EXISTS (
    SELECT 1 FROM sensor s
    WHERE s.microcontroller_id = m.id
    AND s.function = 'humidity'
);

INSERT INTO sensor (function, model, unit_measureament, status, microcontroller_id)
SELECT 'luminosity', 'Sensor de luminosidade', 'lux', 'ACTIVE', m.id
FROM microcontroller m
WHERE m.mac_address = 'AA:BB:CC:00:00:01'
AND NOT EXISTS (
    SELECT 1 FROM sensor s
    WHERE s.microcontroller_id = m.id
    AND s.function = 'luminosity'
);

INSERT INTO sensor (function, model, unit_measureament, status, microcontroller_id)
SELECT 'counter', 'Sensor contador', 'un', 'ACTIVE', m.id
FROM microcontroller m
WHERE m.mac_address = 'AA:BB:CC:00:00:01'
AND NOT EXISTS (
    SELECT 1 FROM sensor s
    WHERE s.microcontroller_id = m.id
    AND s.function = 'counter'
);

-- Microcontrolador 02
INSERT INTO sensor (function, model, unit_measureament, status, microcontroller_id)
SELECT 'temperature', 'Sensor de temperatura', '°C', 'ACTIVE', m.id
FROM microcontroller m
WHERE m.mac_address = 'AA:BB:CC:00:00:02'
AND NOT EXISTS (
    SELECT 1 FROM sensor s
    WHERE s.microcontroller_id = m.id AND s.function = 'temperature'
);

INSERT INTO sensor (function, model, unit_measureament, status, microcontroller_id)
SELECT 'humidity', 'Sensor de umidade', '%', 'ACTIVE', m.id
FROM microcontroller m
WHERE m.mac_address = 'AA:BB:CC:00:00:02'
AND NOT EXISTS (
    SELECT 1 FROM sensor s
    WHERE s.microcontroller_id = m.id AND s.function = 'humidity'
);

INSERT INTO sensor (function, model, unit_measureament, status, microcontroller_id)
SELECT 'luminosity', 'Sensor de luminosidade', 'lux', 'ACTIVE', m.id
FROM microcontroller m
WHERE m.mac_address = 'AA:BB:CC:00:00:02'
AND NOT EXISTS (
    SELECT 1 FROM sensor s
    WHERE s.microcontroller_id = m.id AND s.function = 'luminosity'
);

INSERT INTO sensor (function, model, unit_measureament, status, microcontroller_id)
SELECT 'counter', 'Sensor contador', 'un', 'ACTIVE', m.id
FROM microcontroller m
WHERE m.mac_address = 'AA:BB:CC:00:00:02'
AND NOT EXISTS (
    SELECT 1 FROM sensor s
    WHERE s.microcontroller_id = m.id AND s.function = 'counter'
);

-- Microcontrolador 03
INSERT INTO sensor (function, model, unit_measureament, status, microcontroller_id)
SELECT 'temperature', 'Sensor de temperatura', '°C', 'ACTIVE', m.id
FROM microcontroller m
WHERE m.mac_address = 'AA:BB:CC:00:00:03'
AND NOT EXISTS (
    SELECT 1 FROM sensor s
    WHERE s.microcontroller_id = m.id AND s.function = 'temperature'
);

INSERT INTO sensor (function, model, unit_measureament, status, microcontroller_id)
SELECT 'humidity', 'Sensor de umidade', '%', 'ACTIVE', m.id
FROM microcontroller m
WHERE m.mac_address = 'AA:BB:CC:00:00:03'
AND NOT EXISTS (
    SELECT 1 FROM sensor s
    WHERE s.microcontroller_id = m.id AND s.function = 'humidity'
);

INSERT INTO sensor (function, model, unit_measureament, status, microcontroller_id)
SELECT 'luminosity', 'Sensor de luminosidade', 'lux', 'ACTIVE', m.id
FROM microcontroller m
WHERE m.mac_address = 'AA:BB:CC:00:00:03'
AND NOT EXISTS (
    SELECT 1 FROM sensor s
    WHERE s.microcontroller_id = m.id AND s.function = 'luminosity'
);

INSERT INTO sensor (function, model, unit_measureament, status, microcontroller_id)
SELECT 'counter', 'Sensor contador', 'un', 'ACTIVE', m.id
FROM microcontroller m
WHERE m.mac_address = 'AA:BB:CC:00:00:03'
AND NOT EXISTS (
    SELECT 1 FROM sensor s
    WHERE s.microcontroller_id = m.id AND s.function = 'counter'
);

-- Microcontrolador 04
INSERT INTO sensor (function, model, unit_measureament, status, microcontroller_id)
SELECT 'temperature', 'Sensor de temperatura', '°C', 'ACTIVE', m.id
FROM microcontroller m
WHERE m.mac_address = 'AA:BB:CC:00:00:04'
AND NOT EXISTS (
    SELECT 1 FROM sensor s
    WHERE s.microcontroller_id = m.id AND s.function = 'temperature'
);

INSERT INTO sensor (function, model, unit_measureament, status, microcontroller_id)
SELECT 'humidity', 'Sensor de umidade', '%', 'ACTIVE', m.id
FROM microcontroller m
WHERE m.mac_address = 'AA:BB:CC:00:00:04'
AND NOT EXISTS (
    SELECT 1 FROM sensor s
    WHERE s.microcontroller_id = m.id AND s.function = 'humidity'
);

INSERT INTO sensor (function, model, unit_measureament, status, microcontroller_id)
SELECT 'luminosity', 'Sensor de luminosidade', 'lux', 'ACTIVE', m.id
FROM microcontroller m
WHERE m.mac_address = 'AA:BB:CC:00:00:04'
AND NOT EXISTS (
    SELECT 1 FROM sensor s
    WHERE s.microcontroller_id = m.id AND s.function = 'luminosity'
);

INSERT INTO sensor (function, model, unit_measureament, status, microcontroller_id)
SELECT 'counter', 'Sensor contador', 'un', 'ACTIVE', m.id
FROM microcontroller m
WHERE m.mac_address = 'AA:BB:CC:00:00:04'
AND NOT EXISTS (
    SELECT 1 FROM sensor s
    WHERE s.microcontroller_id = m.id AND s.function = 'counter'
);

-- Microcontrolador 05
INSERT INTO sensor (function, model, unit_measureament, status, microcontroller_id)
SELECT 'temperature', 'Sensor de temperatura', '°C', 'ACTIVE', m.id
FROM microcontroller m
WHERE m.mac_address = 'AA:BB:CC:00:00:05'
AND NOT EXISTS (
    SELECT 1 FROM sensor s
    WHERE s.microcontroller_id = m.id AND s.function = 'temperature'
);

INSERT INTO sensor (function, model, unit_measureament, status, microcontroller_id)
SELECT 'humidity', 'Sensor de umidade', '%', 'ACTIVE', m.id
FROM microcontroller m
WHERE m.mac_address = 'AA:BB:CC:00:00:05'
AND NOT EXISTS (
    SELECT 1 FROM sensor s
    WHERE s.microcontroller_id = m.id AND s.function = 'humidity'
);

INSERT INTO sensor (function, model, unit_measureament, status, microcontroller_id)
SELECT 'luminosity', 'Sensor de luminosidade', 'lux', 'ACTIVE', m.id
FROM microcontroller m
WHERE m.mac_address = 'AA:BB:CC:00:00:05'
AND NOT EXISTS (
    SELECT 1 FROM sensor s
    WHERE s.microcontroller_id = m.id AND s.function = 'luminosity'
);

INSERT INTO sensor (function, model, unit_measureament, status, microcontroller_id)
SELECT 'counter', 'Sensor contador', 'un', 'ACTIVE', m.id
FROM microcontroller m
WHERE m.mac_address = 'AA:BB:CC:00:00:05'
AND NOT EXISTS (
    SELECT 1 FROM sensor s
    WHERE s.microcontroller_id = m.id AND s.function = 'counter'
);
