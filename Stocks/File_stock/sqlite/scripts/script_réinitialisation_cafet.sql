UPDATE stocks
SET stock = 0,
    etat_stock = 'Épuisé';
delete from suivi_stocks;
delete from ventes_journalieres;