DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS ticket;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE ticket (
  ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
  fk_user_id INTEGER NOT NULL,
  credit INTEGER NOT NULL,
  stage TEXT,
  FOREIGN KEY (fk_user_id) REFERENCES user (id)
);
