CREATE TABLE IF NOT EXISTS donors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userId INTEGER NOT NULL,
    bloodGroup TEXT NOT NULL,
    availableForRequest BOOLEAN NOT NULL DEFAULT 1,
    lastDonation DATE,
    FOREIGN KEY (userId) REFERENCES users (id)
);
