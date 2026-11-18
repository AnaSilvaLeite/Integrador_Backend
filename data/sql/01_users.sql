USE integrador;

INSERT INTO `user` (
    password,
    last_login,
    is_superuser,
    username,
    first_name,
    last_name,
    email,
    is_staff,
    is_active,
    date_joined,
    name,
    type,
    photo
)
SELECT
    'pbkdf2_sha256$600000$integrador_sql_2026$7HHJNaB2QlAj11hb5VX8RRc8yZGVyF5Lt6dQIlRDMZ0=',
    NULL,
    0,
    'senai',
    '',
    '',
    'senai@exemplo.com',
    0,
    1,
    UTC_TIMESTAMP(),
    'SENAI',
    'USER',
    NULL
WHERE NOT EXISTS (
    SELECT 1
    FROM `user`
    WHERE username = 'senai'
);
