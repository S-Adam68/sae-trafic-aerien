-- ============================================================
-- SAE Trafic Aérien — Script SQL de création et insertion
-- Base de données : trafic_aerien_db (MariaDB / MySQL)
-- ============================================================

CREATE DATABASE IF NOT EXISTS trafic_aerien_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE trafic_aerien_db;

-- ============================================================
-- CRÉATION DES TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS gestion_aeroport (
    id   INT          NOT NULL AUTO_INCREMENT,
    nom  VARCHAR(200) NOT NULL,
    pays VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS gestion_piste (
    id           INT          NOT NULL AUTO_INCREMENT,
    numero       VARCHAR(20)  NOT NULL,
    longueur     INT UNSIGNED NOT NULL,
    aeroport_id  INT          NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_piste_aeroport
        FOREIGN KEY (aeroport_id) REFERENCES gestion_aeroport(id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS gestion_compagnie (
    id                  INT          NOT NULL AUTO_INCREMENT,
    nom                 VARCHAR(200) NOT NULL,
    description         TEXT,
    pays_rattachement   VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS gestion_typeavion (
    id                        INT          NOT NULL AUTO_INCREMENT,
    marque                    VARCHAR(100) NOT NULL,
    modele                    VARCHAR(100) NOT NULL,
    description               TEXT,
    image                     VARCHAR(100),
    longueur_piste_necessaire INT UNSIGNED NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS gestion_avion (
    id           INT          NOT NULL AUTO_INCREMENT,
    nom          VARCHAR(200) NOT NULL,
    compagnie_id INT          NOT NULL,
    modele_id    INT          NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_avion_compagnie
        FOREIGN KEY (compagnie_id) REFERENCES gestion_compagnie(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_avion_modele
        FOREIGN KEY (modele_id) REFERENCES gestion_typeavion(id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS gestion_vol (
    id                  INT          NOT NULL AUTO_INCREMENT,
    pilote              VARCHAR(200) NOT NULL,
    datetime_depart     DATETIME(6)  NOT NULL,
    datetime_arrivee    DATETIME(6)  NOT NULL,
    avion_id            INT          NOT NULL,
    aeroport_depart_id  INT          NOT NULL,
    aeroport_arrivee_id INT          NOT NULL,
    piste_arrivee_id    INT          DEFAULT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_vol_avion
        FOREIGN KEY (avion_id) REFERENCES gestion_avion(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_vol_depart
        FOREIGN KEY (aeroport_depart_id) REFERENCES gestion_aeroport(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_vol_arrivee
        FOREIGN KEY (aeroport_arrivee_id) REFERENCES gestion_aeroport(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_vol_piste
        FOREIGN KEY (piste_arrivee_id) REFERENCES gestion_piste(id)
        ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================
-- INSERTION DE DONNÉES DE DÉMONSTRATION
-- ============================================================

-- Aéroports
INSERT INTO gestion_aeroport (nom, pays) VALUES
    ('Charles de Gaulle', 'France'),
    ('Paris Orly',         'France'),
    ('London Heathrow',    'Royaume-Uni'),
    ('Amsterdam Schiphol', 'Pays-Bas'),
    ('Madrid Barajas',     'Espagne'),
    ('Rome Fiumicino',     'Italie');

-- Pistes
INSERT INTO gestion_piste (numero, longueur, aeroport_id) VALUES
    ('09L', 4200, 1),
    ('09R', 2700, 1),
    ('27L', 3600, 1),
    ('08',  3650, 2),
    ('26',  2400, 2),
    ('09L', 3902, 3),
    ('27R', 3660, 3),
    ('18R', 3800, 4),
    ('36L', 3400, 4),
    ('18L', 4350, 5),
    ('32R', 3500, 5),
    ('16R', 3900, 6),
    ('34L', 3600, 6);

-- Compagnies
INSERT INTO gestion_compagnie (nom, pays_rattachement, description) VALUES
    ('Air France',   'France',        'Compagnie nationale française fondée en 1933.'),
    ('British Airways', 'Royaume-Uni','Compagnie nationale britannique, membre de Oneworld.'),
    ('KLM',          'Pays-Bas',      'Royal Dutch Airlines, fondée en 1919.'),
    ('Iberia',       'Espagne',       'Compagnie nationale espagnole, fondée en 1927.'),
    ('ITA Airways',  'Italie',        'Successeur d Alitalia, compagnie nationale italienne.'),
    ('easyJet',      'Royaume-Uni',   'Compagnie low-cost européenne basée à Luton.');

-- Types d'avions
INSERT INTO gestion_typeavion (marque, modele, description, longueur_piste_necessaire) VALUES
    ('Airbus', 'A320',     'Moyen-courrier, capacité ~180 passagers.',   2100),
    ('Airbus', 'A330-300', 'Long-courrier bimoteur, ~290 passagers.',    3000),
    ('Airbus', 'A380',     'Plus grand avion de ligne, ~555 passagers.', 3100),
    ('Boeing', '737-800',  'Moyen-courrier populaire, ~162 passagers.',  2090),
    ('Boeing', '777-300ER','Long-courrier bimoteur, ~396 passagers.',    3050),
    ('Boeing', '787-9',    'Dreamliner long-courrier, ~296 passagers.',  2800);

-- Avions
INSERT INTO gestion_avion (nom, compagnie_id, modele_id) VALUES
    ('F-GKXA', 1, 1),
    ('F-GSQI', 1, 3),
    ('F-HJAZ', 1, 6),
    ('G-EUYA', 2, 1),
    ('G-STBH', 2, 5),
    ('PH-BXA', 3, 4),
    ('PH-BQA', 3, 5),
    ('EC-LQM', 4, 1),
    ('EC-MKL', 4, 2),
    ('EI-DTG', 5, 1),
    ('G-EZWA', 6, 1),
    ('G-EZOP', 6, 1);

-- Vols (exemples)
INSERT INTO gestion_vol (pilote, datetime_depart, datetime_arrivee, avion_id, aeroport_depart_id, aeroport_arrivee_id, piste_arrivee_id) VALUES
    ('Martin Dupont',    '2026-06-11 08:00:00', '2026-06-11 09:00:00', 1,  1, 2, 4),
    ('Sophie Laurent',   '2026-06-11 09:00:00', '2026-06-11 10:30:00', 2,  1, 3, 6),
    ('Pierre Moreau',    '2026-06-11 09:30:00', '2026-06-11 11:00:00', 3,  2, 4, 8),
    ('James Smith',      '2026-06-11 10:00:00', '2026-06-11 11:15:00', 4,  3, 1, 1),
    ('Emma Johnson',     '2026-06-11 11:00:00', '2026-06-11 13:00:00', 5,  3, 5, 10),
    ('Hans Muller',      '2026-06-11 11:00:00', '2026-06-11 12:20:00', 6,  4, 1, 3),
    ('Anna De Vries',    '2026-06-11 12:00:00', '2026-06-11 13:00:00', 7,  4, 3, 7),
    ('Carlos Garcia',    '2026-06-11 12:00:00', '2026-06-11 13:30:00', 8,  5, 6, 12),
    ('Maria Rodriguez',  '2026-06-11 13:00:00', '2026-06-11 15:00:00', 9,  5, 1, 2),
    ('Luca Bianchi',     '2026-06-11 13:00:00', '2026-06-11 15:00:00', 10, 6, 2, 5),
    ('Tom Wilson',       '2026-06-11 14:00:00', '2026-06-11 15:40:00', 11, 1, 4, 9),
    ('Julie Petit',      '2026-06-11 14:30:00', '2026-06-11 15:45:00', 12, 2, 3, 7);
