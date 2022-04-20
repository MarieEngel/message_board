from django.test import TestCase


class TestPost(TestCase):

    fixtures = [
        "user_test.json",
        "category_test.json",
        "post_test.json",
        "comment_test.json",
    ]

    def test_add_post(self):
        """Tests if a post created will show up on the home page."""
        self.client.login(username="anna", password="password")
        response = self.client.post(
            "/post/add/",
            {
                "title": "Some title",
                "body": "Some text",
                "category": 1,
                "_save": "SAVE",
            },
        )
        self.assertRedirects(response, "/")
        response = self.client.get("/")
        self.assertContains(response, "Some title")

    def test_delete_post(self):
        """Tests if a deleted post will not show up on the home page."""
        self.client.login(username="anna", password="password")
        response = self.client.get("/post/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Has anybody seen my cow")

        response = self.client.post("/post/1/delete/", follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/")
        self.assertNotContains(response, "Has anybody seen my cow")

    def test_update_post(self):
        """Tests if an updated post will show up on the home page."""
        self.client.login(username="anna", password="password")
        response = self.client.get("/post/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Has anybody seen my cow")
        self.assertNotContains(response, "Has anybody seen my crow")
        response = self.client.post(
            "/post/1/update/",
            {
                "title": "Has anybody seen my crow",
                "body": "My lovely crow is missing.",
                "category": 1,
                "_save": "SAVE",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/")
        self.assertContains(response, "Has anybody seen my crow")

    def test_add_post_anonymous_user(self):
        """Tests if a not logged in user can add a post."""
        response = self.client.get("/post/add/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/post/add/")

    def test_delete_post_anonymous_user(self):
        """Tests if a not logged in user can delete a post."""
        response = self.client.get("/post/1/delete/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/post/1/delete/")

    def test_update_post_anonymous_user(self):
        """Tests if a not logged in user can update a post."""
        response = self.client.get("/post/1/update/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/post/1/update/")

    def test_delete_post_unauthorized_user(self):
        """Tests if a user that is not the author can delete a post."""
        self.client.login(username="marie", password="password")
        response = self.client.get("/post/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Has anybody seen my cow")
        response = self.client.post(
            "/post/1/delete/",
            {"_save": "SAVE"},
        )
        self.assertEqual(response.status_code, 403)
        response = self.client.get("/post/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Has anybody seen my cow")

    def test_update_post_unauthorized_user(self):
        """Tests if a user that is not the author can update a post."""
        self.client.login(username="marie", password="password")
        response = self.client.get("/post/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Has anybody seen my cow")
        self.assertNotContains(response, "Has anybody seen my crow")
        response = self.client.post(
            "/post/1/update/",
            {
                "title": "Has anybody seen my crow",
                "body": "My lovely crow is missing.",
                "category": 1,
                "_save": "SAVE",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 403)
        response = self.client.get("/post/1/")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Has anybody seen my crow")
        self.assertContains(response, "Has anybody seen my cow")
