DROP TABLE IF EXISTS users;

CREATE TABLE users (
  email VARCHAR(30) NOT NULL, 
  password VARCHAR(100) NOT NULL, 
  PRIMARY KEY (email), 
  UNIQUE (email), 
  UNIQUE (password)
)

DROP TABLE IF EXISTS basicTask;

CREATE TABLE "basicTask" (
  "task_id" INTEGER NOT NULL UNIQUE,
  "user_id" INTEGER NOT NULL,
  "name"  VARCHAR NOT NULL,
  "date"  VARCHAR NOT NULL,
  "repetition"  VARCHAR NOT NULL,
  "days"  VARCHAR NOT NULL,
  "months"  VARCHAR NOT NULL,
  UNIQUE("task_id"),
  PRIMARY KEY("task_id" AUTOINCREMENT)
)

DROP TABLE IF EXISTS FacebookTask;

CREATE TABLE "FacebookTask" (
  task_id INTEGER NOT NULL, 
  message VARCHAR NOT NULL, 
  files VARCHAR NOT NULL, 
  PRIMARY KEY (task_id), 
  UNIQUE (task_id), 
  UNIQUE (message), 
  UNIQUE (files)
)

DROP TABLE IF EXISTS InstagramTask;

CREATE TABLE "InstagramTask" (
  task_id INTEGER NOT NULL, 
  message VARCHAR NOT NULL, 
  files VARCHAR NOT NULL, 
  PRIMARY KEY (task_id), 
  UNIQUE (task_id), 
  UNIQUE (message), 
  UNIQUE (files)
)

DROP TABLE IF EXISTS TwitterTask;

CREATE TABLE "TwitterTask" (
  task_id INTEGER NOT NULL, 
  message VARCHAR NOT NULL, 
  files VARCHAR NOT NULL, 
  PRIMARY KEY (task_id), 
  UNIQUE (task_id), 
  UNIQUE (message), 
  UNIQUE (files)
)