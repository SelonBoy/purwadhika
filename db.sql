CREATE DATABASE IF NOT EXISTS `finance_tracker`;
USE `finance_tracker`;

-- =========================
-- TABLE USERS
-- =========================

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nama` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
);

-- =========================
-- TABLE INCOME
-- =========================

DROP TABLE IF EXISTS `income`;

CREATE TABLE `income` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `tanggal` date NOT NULL,
  `sumber` varchar(100),
  `jumlah` int NOT NULL,

  PRIMARY KEY (`id`),

  CONSTRAINT `income_fk_user`
  FOREIGN KEY (`user_id`)
  REFERENCES `users` (`id`)
  ON DELETE CASCADE
);

-- =========================
-- TABLE EXPENSES
-- =========================

DROP TABLE IF EXISTS `expenses`;

CREATE TABLE `expenses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `tanggal` date NOT NULL,
  `kategori` varchar(100),
  `jumlah` int NOT NULL,
  `catatan` text,

  PRIMARY KEY (`id`),

  CONSTRAINT `expenses_fk_user`
  FOREIGN KEY (`user_id`)
  REFERENCES `users` (`id`)
  ON DELETE CASCADE
);

-- =========================
-- OPTIONAL INDEX (OPTIMIZATION)
-- =========================

CREATE INDEX idx_income_user 
ON income(user_id);

CREATE INDEX idx_expense_user 
ON expenses(user_id);

-- =========================
-- OPTIONAL SAMPLE DATA
-- (BOLEH DIHAPUS KALAU MAU FRESH)
-- =========================

--INSERT INTO users (nama) VALUES
--('Michael'),
--('Test User');

--INSERT INTO income (user_id,tanggal,sumber,jumlah) VALUES
--(1,'2026-02-01','Gaji',5000000),
--(1,'2026-02-15','Freelance',1500000);

--INSERT INTO expenses (user_id,tanggal,kategori,jumlah,catatan) VALUES
--(1,'2026-02-02','Makanan',50000,'Nasi padang'),
--(1,'2026-02-03','Transportasi',30000,'Ojek'),
--(1,'2026-02-05','Belanja/Hiburan',120000,'Game');

-- =========================
-- END FILE
-- =========================