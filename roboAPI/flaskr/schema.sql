-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS posts;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  pubkey TEXT NOT NULL,
  sigkey TEXT NOT NULL
);

CREATE TABLE posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  recipient INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  message TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
