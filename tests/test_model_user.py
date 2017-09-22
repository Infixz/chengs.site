# coding: utf-8

import unittest
from app.models import User


class ModelUserTestCase(unittest.TestCase):
    def test_passwd_setter(self):
        user1 = User(password="best")
        self.assertTrue(user1.password_hash is not None)

    def test_no_password_getter(self):
        user1 = User(password="best")
        with self.assertTrueRaises(AttributeError):
            user1.password

    def test_password_verification(self):
        user1 = User(password="best")
        self.assertTrue(user1.verify_password("best"))
        self.assertFalse(user1.verify_password("worst"))

    def test_password_salts_are_random(self):
        user1 = User(password="best")
        user2 = User(password="best")
        self.assertTrue(user1.password_hash != user2.password_hash)
