# from django.test import TestCase
# from django.contrib.auth.models import User


# class TestSearch(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_superuser(
#             username="testuser", password="password"
#         )

#     def tearDown(self):
#         self.user.delete()

#     def test_search_logged_out(self):
#         """Tests that logged out users can't search."""
#         response = self.client.get("/", follow=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Login")
#         self.assertContains(response, "Register")

    