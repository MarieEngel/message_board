from django.test import TestCase


class TestSearch(TestCase):
    fixtures = [
        "user_test.json",
        "category_test.json",
        "post_test.json",
        "comment_test.json",
    ]

    def test_search_anonymous_user(self):
        """Tests that logged out users can't search."""
        response = self.client.get("/post/search?query=das", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")
        self.assertContains(response, "Register")

    def test_search(self):
        """Tests that logged in users can search."""
        self.client.login(username="marie", password="password")
        response = self.client.get("/post/search?query=cow&categories=All", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My lovely cow is missing")
        self.assertContains(response, "My cow is lost again")
        self.assertNotContains(response, "I have lost my cat")
        self.assertNotContains(response, "Silly post")
        self.assertNotContains(response, "Demo")
