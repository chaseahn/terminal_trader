import sqlite3
import hashlib
from model import SALT
from model import pass_hash
import time

def run(dbname="terminal_trader.db"):
    conn = sqlite3.connect(dbname)
    cur  = conn.cursor()

    password = pass_hash('cookiemonster')

    SQL = """INSERT INTO accounts 
        (username, email, firstname, lastname, account_id,
        pw_hash, account_bal, admin_status) 
        VALUES
        (?, ?, ?, ?, ?, ?, ?, ?); """

    cur.execute(SQL, ('terminal_master', 'master@terminal.com', 'MASTER', 'ACCOUNT',
                      '0000000001', password, 0.0, 'ADMIN'))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    run()
