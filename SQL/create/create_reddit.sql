DROP TABLE IF EXISTS reddit;

CREATE TABLE IF NOT EXISTS reddit(
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(30),
  thread VARCHAR(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  href VARCHAR(300),
  link VARCHAR(300),
  comment VARCHAR(300),
  loadtime TIMESTAMP,
  FOREIGN KEY (username) REFERENCES users(username)
);

TRUNCATE TABLE reddit;