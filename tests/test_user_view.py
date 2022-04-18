from http import client
from urllib import response
from django.test import TestCase
from django.urls import reverse

from user.forms import UserRegisterForm

class BaseTest(TestCase):
    
    fixtures = [
    "user_test.json",
    "category_test.json",
    "post_test.json",
    "comment_test.json",
      ]
    
    def setUp(self):
        self.register_url=reverse('user:register')
        self.user={
          'username':'anya',
          'email':'m@email.com'
        }
        return super().setUp()

class TestRegister(BaseTest):
     
    def test_can_view_page_correctly(self):
        response=self.client.get(self.register_url) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/register.html')
      
    def test_after_rigister_redirect(self):
        
        response=self.client.post(self.register_url, self.user, form=UserRegisterForm)
        
        self.assertEqual(response.status_code, 200)
        
class DeleteUser(BaseTest):
      
    def test_delete_user(self):
        self.client.login(username='anya', password='password') 
        
        response=self.client.get("/user/delete/")
        self.assertEqual(response.
        status_code, 200)   
        
        response=self.client.post("/user/login/?next=/")
        self.assertEqual(response.
        status_code, 200)  
        
        self.client.login(username='anya', 
        password='password') 
        response=self.client.get("/user/login/?next=/")        
        
    def user_profile(self):
          
        self.client.login(username='anya', password='password') 
        
        response=self.client.get("/user/profile/")
        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, "user/profile.html")  
        