from django.test import TestCase
from django.test.client import Client
from lieswetellourselves.lies.models import Lie
from django.utils.html import escape

class TestLie(TestCase):
    fixtures = ['data.json']

    def testMainPage(self):
        res = self.client.get('/lies/')
        self.assertContains(res, "Google App Engine Rocks", 1)
        self.assertContains(res, escape("I'm not worried about dying"), 1)
        self.assertContains(res, 'I get angry for good reasons', 1)

    def testAdd(self):
        lieString = 'This test failed'
        res = self.client.post('/lies/add/', { 'lie': lieString })
        testLie = Lie.objects.all().filter(lie=lieString)
        self.assertRedirects(res, '/lies/%i/' % testLie[0].id)
        res = self.client.get('/lies/')
        self.assertContains(res, lieString, 1)

    def testAjaxAddVote(self):
        res = self.client.post('/lies/add_vote/', {'lie_id': '1', 'vote': 'up'},HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        testLie = Lie.objects.all().filter(id=1)[0]
        self.assertEquals(testLie.vote_total(), 1)
        self.client = Client()
        res = self.client.post('/lies/add_vote/', {'lie_id': 1, 'vote': 'up'},HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(testLie.vote_total(), 2)
        self.client = Client()
        res = self.client.post('/lies/add_vote/', {'lie_id': 1, 'vote': 'down'},HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(testLie.vote_total(), 1)
        self.client = Client()
        res = self.client.post('/lies/add_vote/', {'lie_id': 1, 'vote': 'boo'},HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(testLie.vote_total(), 1)
        self.assertContains(res, '"id": 1')
        self.assertContains(res, '"vote_total_value": 1')

    def testAddVote(self):
        res = self.client.post('/lies/add_vote/', {'lie_id': '1', 'vote': 'up'})
        testLie = Lie.objects.all().filter(id=1)[0]
        self.assertEquals(testLie.vote_total(), 1)
        self.client = Client()
        res = self.client.post('/lies/add_vote/', {'lie_id': 1, 'vote': 'up'})
        self.assertEquals(testLie.vote_total(), 2)
        self.client = Client()
        res = self.client.post('/lies/add_vote/', {'lie_id': 1, 'vote': 'down'})
        self.assertEquals(testLie.vote_total(), 1)
        self.client = Client()
        res = self.client.post('/lies/add_vote/', {'lie_id': 1, 'vote': 'boo'})
        self.assertEquals(testLie.vote_total(), 1)
        self.assertRedirects(res, '/lies/')

    def testVoteOnMissingLie(self):
        res = self.client.post('/lies/add_vote/', {'lie_id': 999, 'vote': 'up'})
        self.assertNotEquals(res, None)
        self.assertRedirects(res, '/lies/')

    def testVoteOnce(self):
        res = self.client.post('/lies/add_vote/', {'lie_id': 1, 'vote': 'up'})
        testLie = Lie.objects.all().filter(id=1)[0]
        self.assertEquals(testLie.vote_total(), 1)
        res = self.client.post('/lies/add_vote/', {'lie_id': 1, 'vote': 'up'})
        self.assertEquals(testLie.vote_total(), 1)
        self.client = Client()
        res = self.client.post('/lies/add_vote/', {'lie_id': 1, 'vote': 'up'})
        self.assertEquals(testLie.vote_total(), 2)
        
