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
        sel.open("/")
        try: self.failUnless(sel.is_element_present("id_lie"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.failUnless(sel.is_element_present("add_lie_submit"))
        except AssertionError, e: self.verificationErrors.append(str(e))

    def test_enterLie(self):
        sel = self.selenium
        sel.open('/')
        sel.type('id_lie', 'Testing Via Selenium')
        sel.click('add_lie_submit')
        sel.set_speed(1000)
        self.assertEqual('Testing Via Selenium', sel.get_text("//li[1]/span[2]"))

    def test_enterLieOnEnterPress(self):
        sel = self.selenium
        sel.open('/')
        sel.type('id_lie', 'Testing Via Selenium')
        sel.key_press('id_lie', r'\13')
        sel.set_speed(1000)
        self.assertEqual('Testing Via Selenium', sel.get_text("//li[1]/span[2]"))

    def test_voteSystem(self):
        sel = self.selenium
        sel.set_speed("200")
        sel.open("/")
        self.assertEqual("0", sel.get_text("//li[@id='lie_4']/span[1]"))
        sel.mouse_over("//li[@id='lie_4']")
        sel.click("//a[@id='vote_up']/img")
        self.assertEqual("1", sel.get_text("//li[@id='lie_4']/span[1]"))
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)
        self.stop_test_server()

if __name__ == "__main__":
    unittest.main()

