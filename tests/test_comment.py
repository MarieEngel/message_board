from django.test import TestCase


class CommentTestCase(TestCase):
    fixtures = [
        "user_test.json",
        "category_test.json",
        "post_test.json",
        "comment_test.json",
    ]

    def test_add_comment(self):
        self.client.login(username="anna", password="password")
        response = self.client.get("/post/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Has anybody seen my cow")
        self.assertNotContains(response, "This is test comment")
        response = self.client.post(
            "/post/1/comment/",
            {"body": "This is test comment", "_save": "SAVE"},
        )
        self.assertRedirects(response, "/post/1/#comment-7")
        response = self.client.get("/post/1/#comment-7/")
        self.assertContains(response, "This is test comment")
        response = self.client.get("/post/1/")
        self.assertContains(response, "This is test comment")
