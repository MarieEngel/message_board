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
