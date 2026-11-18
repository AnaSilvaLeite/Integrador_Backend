
USE integrador;

INSERT INTO environment (point, name, description)
SELECT 'PONTO01', 'Corredor 01',
       'Corredor próximo ao laboratório de informática 01'
WHERE NOT EXISTS (
    SELECT 1 FROM environment WHERE point = 'PONTO01'
);

INSERT INTO environment (point, name, description)
SELECT 'PONTO02', 'Corredor 02',
       'Corredor próximo ao laboratório de informática 02'
WHERE NOT EXISTS (
    SELECT 1 FROM environment WHERE point = 'PONTO02'
);

INSERT INTO environment (point, name, description)
SELECT 'PONTO03', 'Corredor 03',
       'Corredor próximo ao laboratório de informática 03'
WHERE NOT EXISTS (
    SELECT 1 FROM environment WHERE point = 'PONTO03'
);

INSERT INTO environment (point, name, description)
SELECT 'PONTO04', 'Corredor 04',
       'Corredor próximo ao laboratório de informática 04'
WHERE NOT EXISTS (
    SELECT 1 FROM environment WHERE point = 'PONTO04'
);

INSERT INTO environment (point, name, description)
SELECT 'PONTO05', 'Corredor 05',
       'Corredor próximo ao laboratório de informática 05'
WHERE NOT EXISTS (
    SELECT 1 FROM environment WHERE point = 'PONTO05'
);
