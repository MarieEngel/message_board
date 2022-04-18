from audioop import reverse
from urllib import response
from django.test import TestCase ,Client
from django.urls import reverse_lazy
from post.models import Post

class HomePageTest(TestCase):


      fixtures = [
      "user_test.json",
      "category_test.json",
      "post_test.json",
      "comment_test.json",
        ]
        
        
        
      def test_home(self):
          '''test homepage, post home view'''
          self.client.login(username="anya", 
          password="password")
          response=self.client.get("")
          self.assertEqual(response.
          status_code, 200)   
         
         
         


      
      
      
      
    
      
      
      