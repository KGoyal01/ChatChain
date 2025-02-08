import sqlite3
con = sqlite3.connect("ledger.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS transact(sender, recipient, quantity, type)")
cur.execute("CREATE TABLE IF NOT EXISTS messages(fromm, too, message)")
cur.execute("CREATE TABLE IF NOT EXISTS phonebook(pnumber,name)")
