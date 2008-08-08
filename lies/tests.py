from django.test import TestCase
from lieswetellourselves.lies.models import Lie
from django.utils.html import escape

class TestLie(TestCase):
    fixtures = ['data.json']

    def testMainPage(self):
        response = self.client.get('/lies/')
        self.assertContains(response, "Google App Engine Rocks", 1)
        self.assertContains(response, escape("I'm not worried about dying"), 1)
        self.assertContains(response, 'I get angry for good reasons', 1)

    def testAdd(self):
        lieString = 'This test failed'
        response = self.client.post('/lies/add/', { 'lie': lieString })
        testLie = Lie.objects.all().filter(lie=lieString)
        self.assertRedirects(response, '/lies/%i/' % testLie[0].id)
        response = self.client.get('/lies/')
        self.assertContains(response, lieString, 1)

