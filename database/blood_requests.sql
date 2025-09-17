CREATE TABLE IF NOT EXISTS blood_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userId INTEGER NOT NULL,
    pint INTEGER NOT NULL,
    address TEXT NOT NULL,
    reason TEXT NOT NULL,
    response TEXT,
    bloodGroup TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    FOREIGN KEY (userId) REFERENCES users (id)
);
