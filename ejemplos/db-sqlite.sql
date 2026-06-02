PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE `alumnos` (
  `id` integer NOT NULL primary key autoincrement,
  `nombre` varchar(20) DEFAULT NULL,
  `apellidos` varchar(50) DEFAULT NULL,
  `edad` integer DEFAULT NULL
);
INSERT INTO alumnos VALUES(1,'Luis','Ferreira',46);
INSERT INTO alumnos VALUES(2,'Juan','Palomo',16);
CREATE TABLE `calificaciones` (
  `id` integer NOT NULL primary key autoincrement,
  `alumnoId` integer NOT NULL,
  `valor` decimal(4,2) DEFAULT NULL
);
INSERT INTO calificaciones VALUES(1,1,5.450000000000000177);
INSERT INTO calificaciones VALUES(2,2,7);
PRAGMA writable_schema=ON;
CREATE TABLE IF NOT EXISTS sqlite_sequence(name,seq);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('alumnos',2);
INSERT INTO sqlite_sequence VALUES('calificaciones',2);
PRAGMA writable_schema=OFF;
COMMIT;
