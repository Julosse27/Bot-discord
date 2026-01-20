import sqlite3 as sqlite
from Stocks.File_stock.Recup_fichiers import recup_sqlite, recup_script_sql

conn = sqlite.connect(recup_sqlite("donnees_stock_cafet.sq3"))
cur = conn.cursor()

cur.executescript(recup_script_sql("script_création_cafet"))

cur.close()
conn.close()