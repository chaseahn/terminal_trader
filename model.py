import sqlite3
import opencursor
from opencursor import OpenCursor
from json.decoder import JSONDecodeError
import requests
import hashlib
import time
from random import randint

#refer to LOOKUPPRICE Function
API_URL = "https://api.iextrading.com/1.0/stock/{}/quote"
opencursor.setDB('terminal_trader.db')
#refer to HASH function
SALT = "BANANANANANANANANANA"
#length of ACCOUNT ID digits
ACC_ID_DIG = 10

HC = .01

def pass_hash(string):
    hasher = hashlib.sha256()
    hasher.update((SALT+string).encode('utf-8'))
    return hasher.hexdigest()

def lookup_price(symbol):
    results = requests.get(API_URL.format(symbol))
    data = results.json()['latestPrice']
    return data

def generate_account_id():
    minimum = 10**(ACC_ID_DIG-1)
    maximum = (10**ACC_ID_DIG)-1
    return randint(minimum,maximum)

def id_exist(idnum):
    with OpenCursor() as cur:
        SQL = """ SELECT * FROM accounts 
              WHERE account_id=?; """
        cur.execute(SQL,(idnum,))
        row = cur.fetchone()
    return bool(row)

def new_id():
    new_id = generate_account_id()
    while id_exist(new_id):
        new_id = generate_account_id()
    return new_id

class Account:

    def __init__(self, row={}, username='', password=''):
        if username:
            self.check_cred(username,password)
        else:
            self.row_set(row)
    
    def row_set(self,row={}):
        row               = dict(row)
        self.pk           = row.get('pk')
        self.firstname    = row.get('firstname')
        self.lastname     = row.get('lastname')
        self.username     = row.get('username')
        self.email        = row.get('email')
        self.account_id   = row.get('account_id')
        self.account_bal  = row.get('account_bal',0.0)
        self.pw_hash      = row.get('pw_hash')
        self.admin_status = row.get('admin_status')
    
    def get_balance(self,user,pw):
        pw_hash = pass_hash(pw)
        with OpenCursor() as cur:
            SQL = """ SELECT account_bal FROM accounts 
                  WHERE username=? AND pw_hash=?; """
            val = (user,pw_hash)
            cur.execute(SQL,val)
            row = cur.fetchone()
            bal = float(row['account_bal'])
        return round(bal, 2)
       
    def check_cred(self,username,password):
        pw_hash = pass_hash(password)
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM accounts WHERE
                  username=? and pw_hash=?; """
            val = (username,pw_hash)
            cur.execute(SQL,val)
            row = cur.fetchone()
        if row:
            self.row_set(row)
        else:
            self.row_set({})
    
    def set_account_id(self):
        self.account_id = new_id()

    def __bool__(self):
        #if self.pk exists bool will return TRUE
        #if not bool returns NONE
        return bool(self.pk)

    def get_all_positions(self):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM positions WHERE account_pk=?; """
            cur.execute(SQL, (self.pk,))
            data = cur.fetchall()
        return [Position(rows) for rows in data]
  
    def get_position(self,symbol):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM positions WHERE account_pk=?
                  AND symbol=?; """
            val = (self.pk,symbol)
            cur.execute(SQL,val)
            row = cur.fetchone()
        if row:
            return Position(row)
        else:
            new_p            = Position()
            new_p.symbol     = symbol
            new_p.shares     = 0
            new_p.account_pk = self.pk
            return new_p
    
    def update_pw(self,new_pw):
        self.pw_hash = pass_hash(new_pw)
        self.save()
    
    def check_un(self,username):
        with OpenCursor() as cur:
            SQL = """ SELECT username FROM accounts WHERE username=?; """
            val = (username,)
            cur.execute(SQL,val)
            row = cur.fetchone()
        if row:
            return bool(row)
    
    def check_em(self,em):
        with OpenCursor() as cur:
            SQL = """ SELECT email FROM accounts WHERE email=?; """
            val = (em,)
            cur.execute(SQL,val)
            row = cur.fetchone()
        if row:
            return bool(row)

    def update_em(self,em):
        self.email = em
        self.save()
    
    def update_un(self,username):
        self.username = username
        self.save()
    
    def master_accounts(self):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM accounts WHERE admin_status=?; """
            cur.execute(SQL, ('NOT_ADMIN',))
            data = cur.fetchall()
        return [Account(rows) for rows in data]

    def master_positions(self):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM positions WHERE account_pk!=?; """
            cur.execute(SQL, (1,))
            data = cur.fetchall()
        return [Position(rows) for rows in data]

    def master_history(self):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM trades WHERE account_pk!=? ORDER BY time DESC ; """
            cur.execute(SQL, (1,))
            data = cur.fetchall()
        return [Trades(rows)for rows in data]
    
    def __repr__(self):
        bal = round(self.account_bal,2)
        bal = '$'+str(bal)
        output = 'Account: {}, Username: {}, Balance: {}'
        return output.format(self.pk,self.username,bal)

    def see_trade_history(self):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM trades WHERE account_pk=?
                  ORDER BY time DESC; """
            cur.execute(SQL,(self.pk,))
            data = cur.fetchall()
        return [Trades(rows) for rows in data]
    
    def see_trade_for(self,symbol):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM trades WHERE account_pk=?
                  AND symbol=? ORDER BY time DESC; """
            val = (self.pk,symbol)
            cur.execute(SQL,val)
            data = cur.fetchall()
        return [Trades(rows) for rows in data]

    def increase_shares(self,symbol,shares):
        inc         = self.get_position(symbol)
        inc.shares += int(shares)
        inc.save()
    
    def decrease_shares(self,symbol,shares):
        dec = self.get_position(symbol)
        if dec.shares < int(shares):
            raise ValueError
        dec.shares -= int(shares)
        dec.save()
    
    def make_trade(self,symbol,shares,user_price): #APPL,3,600
        trade            = Trades()
        trade.account_pk = self.pk
        trade.symbol     = symbol
        trade.shares     = shares
        trade.price      = user_price
        trade.save()
    
    def buy(self,symbol,shares,price=None):
        num = shares.isdigit()
        if not num:
            raise TypeError
        symbol = symbol.upper()
        if not price:
            price = float(lookup_price(symbol))
        total_price = int(shares)*float(price)
        user_price  = float(total_price) * (1+HC)
        skim_amount = float(user_price) - float(total_price)
        if self.account_bal < user_price:
            raise ValueError
        self.increase_shares(symbol,shares)
        self.make_trade(symbol,shares,user_price)
        self.account_bal -= user_price
        self.master_balance(skim_amount)
        self.save()
    
    def sell(self,symbol,shares,price=None):
        num = shares.isdigit()
        if not num:
            raise TypeError
        symbol = symbol.upper()
        if not price:
            price = lookup_price(symbol)
        total_price = int(shares)*float(price)
        user_price  = float(total_price) * (1-HC)
        skim_amount = float(total_price) * HC
        self.decrease_shares(symbol,shares)
        self.make_trade(symbol,-int(shares),user_price)
        self.account_bal += user_price
        self.master_balance(skim_amount)
        self.save()
    
    def get_master(self):
        with OpenCursor() as cur:
            SQL = """ SELECT * FROM accounts WHERE pk=?; """
            val = (1,)
            cur.execute(SQL,val)
            row = cur.fetchone()
            return Account(row)
    
    def master_balance(self,skim_amount):
        master = self.get_master()
        master.account_bal += float(skim_amount)
        master.save()

    # def master_trade(self,skim_amount,symbol):
    #     master             = MasterSheet()
    #     master.account_pk  = self.pk
    #     master.skim_amount = float(skim_amount)
    #     master.symbol      = symbol
    #     master.trade_pk    = self.trade_pk
    #     master.save()

    def save(self):
        #IF TRUE PK EXISTS AND UPDATE THE ACCOUNT INFO
        #IF NONE CREATE NEW ACCOUNT
        if self:
            with OpenCursor() as cur:
                SQL = """ UPDATE accounts SET
                    username=?,firstname=?,lastname=?,
                    account_id=?,email=?,account_bal=?,pw_hash=?,admin_status=?
                    WHERE pk=?; """
                val = (self.username,self.firstname,self.lastname,
                    self.account_id,self.email,self.account_bal,self.pw_hash,self.admin_status,self.pk)
                cur.execute(SQL,val)
        else:
            with OpenCursor() as cur:
                SQL = """ INSERT INTO accounts(
                    username,firstname,lastname,account_id,email,
                    account_bal,pw_hash,admin_status ) VALUES (
                    ?,?,?,?,?,?,?,?); """
                val = (self.username,self.firstname,self.lastname,
                    self.account_id,self.email,self.account_bal,self.pw_hash,self.admin_status)
                cur.execute(SQL,val)
                self.pk = cur.lastrowid

class Position:

    def __init__(self, row={}):
        row             = dict(row)
        self.pk         = row.get('pk')
        self.symbol     = row.get('symbol')
        self.shares     = row.get('shares')
        self.account_pk = row.get('account_pk')

    def __bool__(self):
        return bool(self.pk)
    
    def save(self):
            if self:
                with OpenCursor() as cur:
                    SQL = """ UPDATE positions SET 
                        account_pk = ?, symbol = ?, shares = ?
                        WHERE pk=?; """
                    val = (self.account_pk, self.symbol, self.shares, self.pk)
                    cur.execute(SQL, val)
            else:
                with OpenCursor() as cur:
                    SQL = """ INSERT INTO positions (
                        account_pk, symbol, shares)
                        VALUES (?, ?, ?); """
                    val = (self.account_pk, self.symbol, self.shares)
                    cur.execute(SQL, val)
                    self.pk = cur.lastrowid
        
    def get_value(self):
        price = lookup_price(self.symbol)
        return price * shares
    
    def __repr__(self):
        output = 'Account: {}, Symbol: {}, Shares: {}'
        return output.format(self.account_pk,self.symbol,self.shares)

class Trades:

    def __init__(self, row={}):
        row             = dict(row)
        self.pk         = row.get('pk')
        self.symbol     = row.get('symbol')
        self.price      = row.get('price')
        self.shares     = row.get('shares')
        self.time       = row.get('time')
        self.account_pk = row.get('account_pk')

    def __bool__(self):
        return bool(self.pk)
    
    def save(self):
        if self:
            with OpenCursor() as cur:
                SQL = """ UPDATE trades SET account_pk=?,symbol=?,
                      price=?,shares=?,time=? WHERE pk=?; """
                val = (self.account_pk, self.symbol, self.price,self.shares, self.time, self.pk)
                cur.execute(SQL,val)
        else:
            if not self.time:
                self.time = int(time.time())
            with OpenCursor() as cur:
                SQL = """ INSERT INTO trades(
                    symbol,price,shares,time,account_pk
                    ) VALUES (?,?,?,?,?); """
                val = (self.symbol,self.price,self.shares,self.time,self.account_pk)
                cur.execute(SQL,val)

    def __repr__(self):
        output = 'Account: {}, Symbol: {}, Volume: {}, Amount: {}, Time: {}'
        return output.format(self.account_pk,self.symbol,self.shares,self.price,self.time)

# class Master:

#     def __init__(self, row={}, username = '', password =''):
#         if username:
#             self.check_cred(username,password)
#         else:
#             self.row_set()
    
#     def __bool__(self):
#         return bool(self.pk)
    
#     def save(self):
#         with OpenCursor() as cur:
#             SQL = """ UPDATE master SET balance=? WHERE pk=?; """
#             val = (self.balance, self.pk)
#             cur.execute(SQL,val)

#     def row_set(self,row={}):
#         row            = dict(row)
#         self.pk        = row.get('pk')
#         self.username  = row.get('username')
#         self.balance   = row.get('balance')
#         self.pw_hash   = row.get('pw_hash')
    
#     def check_cred(self,username,password):
#         pw_hash = pass_hash(password)
#         with OpenCursor() as cur:
#             SQL = """ SELECT * FROM master WHERE
#                   username=? and pw_hash=?; """
#             val = (username,pw_hash)
#             cur.execute(SQL,val)
#             row = cur.fetchone()
#         if row:
#             row            = dict(row)
#             self.pk        = row.get('pk')
#             self.username  = row.get('username')
#             self.balance   = row.get('balance')
#             self.pw_hash   = row.get('pw_hash')
#         else:
#             self.row_set()
       
# class MasterSheet:

#     def __init__(self, row ={}):
#         row              = dict(row)
#         self.pk          = row.get('pk')
#         self.account_pk  = row.get('account_pk')
#         self.symbol      = row.get('symbol')
#         self.skim_amount = row.get('skim_amount')
#         self.trade_pk    = row.get('trade_pk')
    
#     def __bool__(self):
#         return bool(self.pk)
    
#     def save(self):
#         if self:
#             with OpenCursor() as cur:
#                 SQL = """ UPDATE trades SET account_pk=?,skim_amount=?,
#                       symbol=?,trade_pk=? WHERE pk=?; """
#                 val = (self.account_pk, self.skim_amount, self.symbol,self.trade_pk,self.pk)
#                 cur.execute(SQL,val)
#         else:
#             if not self.time:
#                 self.time = int(time.time())
#             with OpenCursor() as cur:
#                 SQL = """ INSERT INTO trades(
#                     account_pk,skim_amount,symbol,trade_pk
#                     ) VALUES (?,?,?,?); """
#                 val = (self.account_pk,self.skim_amount,self.symbol,self.trade_pk)
#                 cur.execute(SQL,val)