from django.test import TestCase
from post.models import Category

class TestPostModel(TestCase):
   def test_model_str(self):
        name= Category.objects.create(name="category")
        self.assertEqual(str(name),"category")
        




   
   
   