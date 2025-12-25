import sqlite3 as sqlite
from Stocks.File_stock.Recup_fichiers import recup_sqlite

conn = sqlite.connect(recup_sqlite("données.sq3"))
cur = conn.cursor()

cur.execute("""create table ventes_journalières(
            capucino integer default 0,
            noisette integer default 0,
            caramel integer default 0,
            citron integer default 0,
            menthe integer default 0,
            café integer default 0,
            chocolat integer default 0,
            date text)""")

cur.close()
conn.close()