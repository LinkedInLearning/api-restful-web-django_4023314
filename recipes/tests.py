from django.contrib.auth.models import User

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase

from recipes.models import Category
from rest_framework.test import APITestCase

from django.test.utils import override_settings

TEST_CACHE_SETTINGS = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

class CategoryViewSetTestCase(APITestCase):

  @override_settings(CACHES=TEST_CACHE_SETTINGS)
  def test_empty_list(self):
    response = self.client.get('/v1/categories/')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data['results']), 0)

  @override_settings(CACHES=TEST_CACHE_SETTINGS)
  def test_list_ordered_categories(self): 
    Category.objects.create(name = 'DEUX' , order = 2)
    Category.objects.create(name = 'UN'   , order = 1)
    Category.objects.create(name = 'TROIS', order = 3)
    
    response = self.client.get('/v1/categories/')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data['results']), 3)
    self.assertListEqual(
      [c['name'] for c in response.data['results']], 
      ['UN', 'DEUX', 'TROIS']
    )

  def test_create_category_anonymous(self):
    response = self.client.post(
        '/v1/categories/',
        {'name': 'Test Category', 'order': 1}
    )
    self.assertEqual(response.status_code, 401)
    self.assertEqual(Category.objects.count(), 0)

  def test_create_category_forbidden(self):
    admin = User.objects.create_user(username='toto', password='P455w0rd')
    jwt = RefreshToken.for_user(admin).access_token
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt}')

    response = self.client.post(
        '/v1/categories/',
        {'name': 'Test Category', 'order': 1}
    )
    self.assertEqual(response.status_code, 403)
    self.assertEqual(Category.objects.count(), 0)

  def test_create_category(self):
    admin = User.objects.create_superuser(username='root', password='P455w0rd')
    jwt = RefreshToken.for_user(admin).access_token
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {jwt}')
 
    response = self.client.post(
      '/v1/categories/', 
      { 'name': 'Test Category', 'order':1 }
    )

    self.assertEqual(response.status_code, 201)
    self.assertDictEqual(response.data, {
      'id': 1,
      'name': 'Test Category',
      'order': 1
    })
    self.assertEqual(Category.objects.count(), 1)
