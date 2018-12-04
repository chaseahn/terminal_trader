import sqlite3
import hashlib
from model import SALT
import time

def run(dbname="terminal_trader.db"):
    conn = sqlite3.connect(dbname)
    cur  = conn.cursor()

    hasher = hashlib.sha512()
    hasher.update((SALT + 'password!').encode('utf-8'))
    pass_hash = hasher.hexdigest()

    SQL = """INSERT INTO accounts 
        (firstname, lastname, account_bal,
        username, pw_hash, account_id) 
        VALUES
        (?, ?, ?, ?, ?, ?); """

    cur.execute(SQL, ('chase1', 'Chase', 'Ahn',
                      '000002', pass_hash, 10000.00))

    SQL = """ INSERT INTO positions
        (symbol, shares, account_pk)
        VALUES
        (?, ?, ?); """

    cur.execute(SQL, (1, 'tsla', 5))

    SQL = """ INSERT INTO trades
        (symbol, price, shares, time, account_pk)
        VALUES
        (?, ?, ?, ?, ?); """

    cur.execute(SQL, (1, 'tsla', 5, 100.00, int(time.time())))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    run()
