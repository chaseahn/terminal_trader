import model
from model import Account, Position, Trade
import schema
import seed
from unittest import TestCase
import os
import time

# to run tests run 'python -m unittest discover tests' in the base directory
# where 'tests' is the name of your tests folder


class TestAccountLoadCreateSave(TestCase):
    def setUp(self):
        schema.run("test.db")
        seed.run("test.db")
        model.opencursor.setDB("test.db")

    def tearDown(self):
        os.remove("test.db")

    def testDictCreate(self):
        vars = {"username": "testuser", "pass_hash": "xxx", "account_id": "01"}
        a = Account(vars)
        self.assertEqual(a.username, "testuser",
                         "property set from initialization with dictionary")
        self.assertEqual(a.balance, 0.0, "balance initialized to 0.0")

    def testCredential(self):
        a = Account(username="carter", password="password!")
        self.assertTrue(a, "Good credentials result in logged in account.")
        badaccount = Account(username="carter", password="wrongpass")
        self.assertFalse(badaccount,
                         "Bad credentials result in False-y account")

    def testNew(self):
        a = Account()
        a.username = "newuser"
        a.set_hashed_password("newpassword")
        a.set_new_id()
        self.assertFalse(a, "unsaved account is False-y")

        a.save()
        self.assertTrue(a, "saved account is Truthy")
        check_id = a.account_id

        b = Account(username="newuser", password="newpassword")
        self.assertEqual(check_id, b.account_id,
                         "load new user from credentials, check account_id")

    def testUpdate(self):
        a = Account(username="carter", password="password!")
        a.balance = 12345.00
        a.save()

        b = Account(username="carter", password="password!")
        self.assertEqual(b.balance, 12345.00, "balance updated after save")


class TestPositionLoadUpdateSave(TestCase):
    def setUp(self):
        schema.run("test.db")
        seed.run("test.db")
        model.opencursor.setDB("test.db")

    def tearDown(self):
        os.remove("test.db")

    def testLoad(self):
        a = Account(username="carter", password="password!")

        p = a.get_position("tsla")
        self.assertTrue(p.amount > 0, "getPosition returns a position")

        p2 = a.get_position("ibm")
        self.assertFalse(p2, "zero position is False")
        self.assertEqual(p2.amount, 0.0, "zero position has zero amount")

    def testUpdate(self):
        a = Account(username="carter", password="password!")

        p = a.get_position("tsla")
        amount = p.amount
        p.amount = p.amount + 4
        p.save()
        p2 = a.get_position("tsla")
        self.assertEqual(p2.amount, amount + 4, "increase in amount is saved.")

    def testIncreaseDecrease(self):
        a = Account(username="carter", password="password!")
        p = a.get_position("tsla")
        amount = p.amount
        with self.assertRaises(
                ValueError,
                msg="decreasing a position by too much raises ValueError"):
            a.decrease_position("tsla", 1000)

        a.increase_position("tsla", 3)
        p2 = a.get_position("tsla")
        self.assertEqual(p2.amount, amount + 3,
                         "increase_position increases a position's amount")

        a.decrease_position("tsla", 2)
        p3 = a.get_position("tsla")
        self.assertEqual(p3.amount, amount + 1,
                         "decrease_position decreases a position")

    def testNewPosition(self):
        a = Account(username="carter", password="password!")
        p = a.get_position("ibm")
        self.assertFalse(p, "non-existent position is False object")
        a.increase_position("ibm", 1)
        p2 = a.get_position("ibm")
        self.assertEqual(p2.amount, 1,
                         "increase position saves a new position")


class TestTradeLoadUpdateSave(TestCase):
    account = None

    def setUp(self):
        schema.run("test.db")
        seed.run("test.db")
        model.opencursor.setDB("test.db")
        self.account = Account(username="carter", password="password!")

    def tearDown(self):
        os.remove("test.db")

    def testNoTrades(self):
        trades = self.account.get_trades_for("ibm")
        self.assertEqual(trades, [],
                         "get_trades_for returns empty list for ibm")

    def testGetTrades(self):
        trades = self.account.get_trades_for("tsla")
        self.assertGreaterEqual(
            len(trades), 1, "get_trades_for returns a list")
        trades2 = self.account.get_trades()
        self.assertGreaterEqual(len(trades2), 1, "get_trades returns a list")

    def testMakeTrade(self):
        trades = self.account.get_trades()
        now = int(time.time())
        self.account.make_trade("f", 3, 10.0)
        trades2 = self.account.get_trades()
        self.assertGreater(len(trades2), len(trades), "trades list has grown")
        self.assertGreaterEqual(trades2[0].time, now,
                                "newest trade has current time")
        fordtrades = self.account.get_trades_for("f")
        self.assertGreaterEqual(
            len(fordtrades), 1, "new trade accessed through symbols")
        self.assertEqual(fordtrades[0].volume, 3, "trade has correct volume")


class TestBuySell(TestCase):
    account = None

    def setUp(self):
        schema.run("test.db")
        seed.run("test.db")
        model.opencursor.setDB("test.db")
        self.account = Account(username="carter", password="password!")

    def tearDown(self):
        os.remove("test.db")

    def testBuy(self):
        funds = self.account.balance
        with self.assertRaises(
                ValueError, msg="buying without enough money raises error"):
            self.account.buy("tsla", 10000, 100.0)
        self.account.buy("ibm", 2, 10.0)
        self.assertEqual(self.account.balance, funds - 20.0,
                         "money removed from account")
        ibmpos = self.account.get_position("ibm")
        self.assertEqual(ibmpos.amount, 2, "buy creates position")
        ibmtrades = self.account.get_trades_for("ibm")
        self.assertEqual(len(ibmtrades), 1, "buy creates a trade")
        self.assertEqual(ibmtrades[0].volume, 2, "trade volume is correct")

    def testSell(self):
        funds = self.account.balance
        tslapos = self.account.get_position("tsla")

        with self.assertRaises(
                ValueError, msg="insufficient shares raises error"):
            self.account.sell("tsla", 100, 100.0)

        self.account.sell("tsla", 1, 100.0)
        self.assertEqual(self.account.balance, funds + 100.0,
                         "sell generates money")

        tslapos2 = self.account.get_position("tsla")
        self.assertEqual(tslapos2.amount, tslapos.amount - 1,
                         "sell reduces position")

        tslatrades = self.account.get_trades_for("tsla")
        self.assertGreater(len(tslatrades), 1, "sell generates new trade")
        self.assertEqual(tslatrades[0].volume, -1,
                         "sell trade has negative volume")
