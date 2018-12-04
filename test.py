import model
from model import Account,Position,Trades
from model import pass_hash
import schema
import seed
from unittest import TestCase
import os
import time

# to run tests run 'python -m unittest discover tests' in the base directory
# where 'tests' is the name of your tests folder

class TestAccLoadCreateSave(TestCase):
    def setUp(self):
        schema.run("test.db")
        seed.run("test.db")
        model.opencursor.setDB("test.db")
    
    def tearDown(self):
        os.remove("test.db")
    
    def testDictCreate(self):
        vars = {"username": "testuser", "pw_hash": "xxx", "account_id": "01"}
        a = Account(vars)
        
        self.assertEqual(a.username, "testuser", "property set from initial with dict.")
        self.assertEqual(a.account_bal, 0.0, "balance initialized")
    
    def testCredential(self):
        a = Account(username = "chase1",password="password!")
        self.assertTrue(a, "Good credentials, logged in account")
        bad_a = Account(username="chase1",password="wrongpassword!")
        self.assertFalse(bad_a, "Bad credentials, false account")

    def testNew(self):
        a = Account()
        a.username = "newuser"
        a.pw_hash  = pass_hash("newpassword")
        a.set_new_id()
        a.firstname = "first"
        a.lastname = "last"
        self.assertFalse(a,"unsaved account is False-y")

        a.save()
        self.assertTrue(a, "new saved account is Truth-y")
        check_id = a.account_id
        check_pw = a.pw_hash

        b = Account(username="newuser",password="newpassword")
        self.assertEqual(check_id,b.account_id,"check equal id from new account")
        self.assertEqual(check_pw,b.pw_hash,"check equal pw from new account")
    
    def testUpdate(self):

        a = Account(username = "chase1",password="password!")
        a.account_bal = 23234343422.0
        a.save()

        b = Account(username = "chase1",password="password!")
        self.assertTrue(b.account_bal, 23234343422.0, "check if saved balance is the same as =")
