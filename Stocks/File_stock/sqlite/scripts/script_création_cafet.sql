CREATE TABLE stocks (
    nom TEXT PRIMARY KEY,
    stock INTEGER DEFAULT 0,
    etat_stock TEXT CHECK(
        etat_stock IN ('Critique', 'Épuisé', 'Bon', 'Très bon', 'Moyen')
    ) DEFAULT 'Épuisé'
);
CREATE TABLE suivi_stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_consommation TEXT,
    quantite INTEGER not NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    annee_scolaire text not NULL,
    FOREIGN KEY (nom_consommation) REFERENCES stocks(id)
);
create table ventes_journalieres(
    stocks_achete json NOT NULL,
    -- format: '[{"nom":"Cappuccino", "qte":10}, ...]'
    date datetime DEFAULT CURRENT_TIMESTAMP,
    annee_scolaire text not NULL
);
CREATE TRIGGER verif_stocks BEFORE
INSERT ON ventes_journalieres BEGIN
SELECT CASE
        WHEN not json_valid(NEW.stocks_achete) = 1 THEN RAISE(
            ABORT,
            "Les stocks doivents être indiqués sous la forme d'un json."
        )
        WHEN NEW.annee_scolaire NOT GLOB '[0-2][0-9][0-9][0-9]-[0-2][0-9][0-9][0-9]' THEN RAISE(ABORT, "L'année donnée n'est pas valide")
        when NOT EXISTS (
            SELECT 1
            from json_each(new.stocks_achete) as je
            WHERE je.value->>'nom' IN (
                    SELECT nom
                    FROM stocks
                )
        ) THEN RAISE(ABORT, "La consommation n'a pas un nom valide.")
        WHEN EXISTS (
            SELECT 1
            FROM json_each(NEW.stocks_achete) as je
            WHERE CAST(je.value->>'qte' as Integer) > (
                    SELECT stock
                    from stocks
                    WHERE je.value->>'nom' = nom
                )
        ) THEN RAISE(ABORT, 'Stock insuffisant')
    END;
END;
CREATE TRIGGER enregistrement_vente
AFTER
INSERT ON ventes_journalieres BEGIN
INSERT INTO suivi_stocks(nom_consommation, quantite, annee_scolaire)
SELECT js.value->>'nom',
    CAST(js.value->>'qte' AS integer),
    NEW.annee_scolaire
from json_each(NEW.stocks_achete) as js;
END;
CREATE TRIGGER maj_stocks
AFTER
INSERT ON suivi_stocks BEGIN
UPDATE stocks
SET stock = stock + NEW.quantite,
    etat_stock = CASE
        WHEN (
            SELECT stock
            FROM stocks
            WHERE nom = NEW.nom_consommation
        ) + NEW.quantite = 0 THEN 'Épuisé'
        WHEN (
            SELECT stock
            FROM stocks
            WHERE nom = NEW.nom_consommation
        ) + NEW.quantite < 41 THEN 'Critique'
        WHEN (
            SELECT stock
            FROM stocks
            WHERE nom = NEW.nom_consommation
        ) + NEW.quantite < 66 THEN 'Moyen'
        WHEN (
            SELECT stock
            FROM stocks
            WHERE nom = NEW.nom_consommation
        ) + NEW.quantite < 101 THEN 'Bon'
        ELSE 'Très bon'
    END
WHERE nom = NEW.nom_consommation;
END;
INSERT INTO stocks(nom)
VALUES ('Cappuccino'),
    ('Noisette'),
    ('Caramel'),
    ('Citron'),
    ('Menthe'),
    ('Cafe'),
    ('Chocolat');