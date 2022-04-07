from django.test import TestCase
from django.contrib.auth.models import User


class TestPost(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="testuser", password="password"
        )

    def tearDown(self):
        self.user.delete()

    def test_add_post(self):
        """Test if a post created will show up on the home page."""
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            "/post/add/",
            {
                "title": "Some title",
                "body": "Some text",
            },
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.get("/")
        self.assertTrue("Some title" in str(response.content))


    def test_delete_post(self):
        """Test if a deleted post will not show up on the home page."""
        self.client.login(username="testuser", password="password")
        self.client.post(
            "/post/add/",
            {
                "title": "To delete",
                "body": "To delete this text",
                "_save": "SAVE"},
        )
        response = self.client.get("/")
        self.assertTrue("To delete" in str(response.content))
        response = self.client.get(
            "/post/1/delete/",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "Are you sure you want to delete this post?" in str(response.content)
        )
        response = self.client.post("/post/1/delete/")
        self.assertEqual(response.status_code, 302)
        self.assertFalse("To delete" in str(response.content))


    def test_update_post(self):
        """Test if an updated post will show up on the home page."""
        self.client.login(username="testuser", password="password")
        self.client.post(
            "/post/add/",
            {
                "title": "Version 1",
                "body": "Text to be updated",
                "_save": "SAVE"},
        )
        response = self.client.get("/")
        self.assertTrue("Version 1" in str(response.content))
        response = self.client.post(
            "/post/1/update/",
            {
                "title": "Version 2",
                "body": "Text to be updated",
                "_save": "SAVE"
            }
        )
        response = self.client.get("/")
        self.assertContains(response, "Version 2")


    # def test_home_view_logged_out(self):
    #     """Tests that logged out users can't see posts."""
    #     response = self.client.get("/", follow=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertNotContains(response, "Latest Posts")


    # def test_add_post_logged_out(self):
    #     """Tests that logged out users can't add posts."""
    #     response = self.client.get("/", follow=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "Login")
    #     self.assertContains(response, "Register")


    def test_delete_post_logged_out(self):
        """Tests that logged out users can't delete posts."""
        self.client.login(username="testuser", password="password")
        self.client.post(
            "/post/add/",
            {
                "title": "To delete",
                "body": "Text to be deleted",
                "_save": "SAVE"},
        )
        response = self.client.get("/")
        self.assertContains(response, "To delete")
        self.client.logout()
        response = self.client.get(
            "/post/1/delete/",
        )
        self.assertEqual(response.status_code, 302)
        self.assertNotContains(response,
            "Are you sure you want to delete this post?")
        

    def test_update_post_logged_out(self):
        """Tests that logged out users can't update posts."""
        self.client.login(username="testuser", password="password")
        self.client.post(
            "/post/add/",
            {
                "title": "Version 1",
                "body": "Text to be updated",
                "_save": "SAVE"},
        )
        response = self.client.get("/")
        self.assertContains(response, "Version 1")
        self.client.logout()
        response = self.client.get(
            "/post/1/update/",
        )
        self.assertEqual(response.status_code, 302)
        self.assertNotContains(response, 
            "Edit")
        


