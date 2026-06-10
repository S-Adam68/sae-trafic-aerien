-- Script de configuration MariaDB — VM2
-- A exécuter en tant que root sur la VM2

CREATE DATABASE IF NOT EXISTS trafic_aerien_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Remplacer [IP_VM1] par l'IP réelle de la VM1 (interface enp0s8, ex: 10.10.10.1)
CREATE USER IF NOT EXISTS 'trafic_user'@'[IP_VM1]' IDENTIFIED BY '[MOT_DE_PASSE]';
GRANT ALL PRIVILEGES ON trafic_aerien_db.* TO 'trafic_user'@'[IP_VM1]';
FLUSH PRIVILEGES;
