from selenium import selenium
from django.test import TestCase
import unittest, time, re

class TestSelenium(TestCase):
    fixtures = ['data.json']
    def setUp(self):
        self.start_test_server('0.0.0.0', 8000)
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*firefox /usr/lib/firefox-3.0.1/firefox", "http://localhost:8000/")
        self.selenium.start()
    
    def test_verifyForm(self):
        sel = self.selenium
        sel.open("/lies/")
        try: self.failUnless(sel.is_element_present("id_lie"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("add_lie_submit"))
        except AssertionError, e: self.verificationErrors.append(str(e))

    def test_voteSystem(self):
        sel = self.selenium
        sel.set_speed("200")
        sel.open("/lies/")
        self.assertEqual("0", sel.get_text("//li[@id='lie_4']/span[1]"))
        sel.mouse_over("//li[@id='lie_4']")
        sel.click("//a[@id='vote_up']/img")
        self.assertEqual("1", sel.get_text("//li[@id='lie_4']/span[1]"))
        sel.click("//a[@id='vote_down']/img")
        self.assertEqual("0", sel.get_text("//li[@id='lie_4']/span[1]"))
        sel.click("//a[@id='vote_down']/img")
        self.assertEqual("-1", sel.get_text("//li[@id='lie_4']/span[1]"))
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)
        self.stop_test_server()

if __name__ == "__main__":
    unittest.main()

