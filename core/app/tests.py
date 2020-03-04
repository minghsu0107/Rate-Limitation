from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase
from app.rateLimit import redis

class DemoLimitRateViewTest(APITestCase):
	'''
	Several tests for the rate limitation app
	'''
	def setUp(self):
		self.url = reverse("demo-limited")
		self.limit = settings.REQUEST_LIMITATION.get('limit', 1000)
		self.window = settings.REQUEST_LIMITATION.get('window', 3600)

	def test_success(self):
		""" Tests requesting up to the limit """
		redis.flushdb()

		for i in range(1, self.limit + 1):
			response = self.client.get(self.url)
			self.assertEqual(response.data['content'], 'success!')
			self.assertEqual(response.status_code, status.HTTP_200_OK)
			self.assertEqual(int(response['X-RateLimit-Limit']), self.limit)
			self.assertEqual(int(response['X-RateLimit-Remaining']), self.limit - i)
			self.assertTrue(int(response['X-RateLimit-Reset']) <= self.window)
			self.assertTrue(int(response['X-RateLimit-Reset']) >= 0)

	def test_rate_exceeded(self):
		""" Tests requesting exceed the limit within the window """
		redis.flushdb()
		
		for i in range(1, self.limit + 1):
			response = self.client.get(self.url)
		
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
		self.assertEqual(response.data['error'], 'API rate limit exceeded')


    
        
        