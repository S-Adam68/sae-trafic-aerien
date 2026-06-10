# Diagramme de Gantt — SAE Trafic Aérien

```mermaid
gantt
    title SAE Trafic Aérien — Planning du projet
    dateFormat  YYYY-MM-DD
    section Analyse & Conception
    Analyse des besoins fonctionnels     :a1, 2026-01-12, 4d
    Modélisation base de données         :a2, after a1, 3d
    Schéma relationnel                   :a3, after a2, 2d
    Maquettes interfaces                 :a4, after a3, 3d

    section Développement Backend
    Création du projet Django            :b1, 2026-01-26, 2d
    Modèles (Aeroport, Piste, Compagnie) :b2, after b1, 3d
    Modèles (TypeAvion, Avion, Vol)      :b3, after b2, 3d
    Logique affectation piste            :b4, after b3, 4d
    Formulaires et validation            :b5, after b4, 3d

    section Développement Frontend
    Template de base et navigation       :c1, 2026-02-09, 3d
    Pages liste et formulaires CRUD      :c2, after c1, 5d
    Tableau de bord et statistiques      :c3, after c2, 2d
    Fiche vols et filtres avancés        :c4, after c3, 3d
    Import CSV en masse                  :c5, after c4, 2d

    section Tests & Corrections
    Tests fonctionnels                   :t1, 2026-03-02, 4d
    Correction des bugs                  :t2, after t1, 3d

    section Déploiement
    Configuration VM2 — MariaDB          :d1, 2026-03-09, 2d
    Configuration VM1 — Nginx/Gunicorn   :d2, after d1, 2d
    Service systemd Gunicorn             :d3, after d2, 1d
    Tests de déploiement                 :d4, after d3, 2d

    section Documentation
    Fiche de procédure                   :e1, 2026-03-16, 3d
    README et dépôt GitHub               :e2, after e1, 2d
    Rapport final                        :e3, after e2, 3d
```

## Résumé du planning

| Phase | Période | Durée |
|---|---|---|
| Analyse & Conception | 12 jan – 23 jan 2026 | 2 semaines |
| Développement Backend | 26 jan – 13 fév 2026 | 3 semaines |
| Développement Frontend | 9 fév – 2 mar 2026 | 3 semaines |
| Tests & Corrections | 2 mar – 6 mar 2026 | 1 semaine |
| Déploiement | 9 mar – 13 mar 2026 | 1 semaine |
| Documentation | 16 mar – 24 mar 2026 | 1,5 semaine |
