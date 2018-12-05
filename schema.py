import sqlite3

CON = None
CUR = None

def setup(dbname='terminal_trader.db'):
    global CON
    global CUR
    CON = sqlite3.connect(dbname)
    CUR = CON.cursor()

def run():
    CUR.execute("""DROP TABLE IF EXISTS accounts;""")
    # create accounts table
    CUR.execute("""CREATE TABLE accounts(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        firstname VARCHAR,
        lastname VARCHAR,
        account_bal FLOAT,
        username VARCHAR,
        email VARCHAR,
        pw_hash VARCHAR,
        account_id VARCHAR,
        admin_status VARCHAR,
        CONSTRAINT unique_email UNIQUE(email),
        CONSTRAINT unique_username UNIQUE(username),
        CONSTRAINT unique_account_id UNIQUE(account_id)
    );""")

    CUR.execute("""DROP TABLE IF EXISTS positions;""")
    # create positions table
    CUR.execute("""CREATE TABLE positions(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol VARCHAR,
        shares INTEGER,
        account_pk INTEGER,
        FOREIGN KEY(account_pk) REFERENCES accounts(pk),
        CONSTRAINT unique_account_symbol UNIQUE (account_pk, symbol)
    );""")

    CUR.execute("""DROP TABLE IF EXISTS trades;""")

    # create trades table
    CUR.execute("""CREATE TABLE trades(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol VARCHAR,
        price FLOAT,
        shares INTEGER,
        time INTEGER,
        account_pk INTEGER,
        FOREIGN KEY(account_pk) REFERENCES accounts(pk)
    );""")

    # CUR.execute("""DROP TABLE IF EXISTS master;""")
    # # create accounts table
    # CUR.execute("""CREATE TABLE master(
    #     pk INTEGER PRIMARY KEY AUTOINCREMENT,
    #     username VARCHAR,
    #     balance FLOAT,
    #     pw_hash VARCHAR,
    #     trade_pk INTEGER,
    #     FOREIGN KEY(trade_pk) REFERENCES trades(pk)
    # );""")

    # CUR.execute("""DROP TABLE IF EXISTS master_sheet;""")
    # # create accounts table
    # CUR.execute("""CREATE TABLE master_sheet(
    #     pk INTEGER PRIMARY KEY AUTOINCREMENT,
    #     account_pk INTEGER,
    #     symbol VARCHAR,
    #     skim_amount FLOAT,
    #     trade_pk INTEGER,
    #     FOREIGN KEY(account_pk) REFERENCES accounts(pk),
    #     FOREIGN KEY(trade_pk) REFERENCES trades(pk)
    # );""")

    CON.commit()
    CUR.close()
    CON.close()

if __name__ == '__main__':
    setup()
    run()