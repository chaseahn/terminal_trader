import model
from model import Account, Position, Trades
import schema
import master_seed
import unittest
import os
import time

# to run tests run 'python -m unittest discover tests' in the base directory
# where 'tests' is the name of your tests folder

class TestAccountCreateAndLoad(unittest.TestCase):
    def setUp(self):
        schema.run("test.db")
        master_seed.run("test.db")
        model.opencursor.setDB("test.db")
        self.account = model.Account(username="terminal_master", password="cookiemonster")
    
    def tearDown(self):
        os.remove("test.db")
    
    def testAccountLoad(self):
        a = model.Account(username="terminal_master", password="cookiemonster")
        self.assertEqual(a.username, "terminal_master", "User loaded from username, password")
        a2 = model.Account(username="terminal_master", password="wrongpassword")
        self.assertFalse(a2, "Bad credentials results in false account object")
    
    def testAccountModify(self):
        a = model.Account(username="terminal_master", password="cookiemonster")
        a.account_bal = 2000.0
        a.save()
        a = model.Account(username="terminal_master", password="cookiemonster")
        self.assertEqual(a.account_bal, 2000.0, "change to balance is saved.")
    
    def testAdminStatus(self):
        a = self.account
        self.assertEqual(a.admin_status, "ADMIN", "status loaded from database")