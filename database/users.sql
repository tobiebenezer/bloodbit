CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    bloodGroup TEXT NOT NULL,
    password TEXT NOT NULL,
    confirmPhone TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL UNIQUE,
    address TEXT NOT NULL,
    gender TEXT NOT NULL
);
