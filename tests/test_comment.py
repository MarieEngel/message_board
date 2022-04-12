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

    def test_update_comment(self):
        self.client.login(username="anna", password="password")
        response = self.client.get("/post/2/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I have lost my cat! Please help")
        self.assertNotContains(response, "This comment has been edited")
        response = self.client.post(
            "/post/2/comment/2/update/",
            {"body": "This comment has been edited", "_save": "SAVE"},
        )
        self.assertRedirects(response, "/post/2/#comment-2")
        response = self.client.get("/post/2/")
        self.assertContains(response, "This comment has been edited")

    def test_delete_comment(self):
        self.client.login(username="marie", password="password")
        response = self.client.get("/post/2/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I have lost my cat! Please help")
        self.assertContains(response, "Another short comment")
        response = self.client.post(
            "/post/2/comment/4/delete/",
            {"_save": "SAVE"},
        )
        self.assertRedirects(response, "/post/2/")
        response = self.client.get("/post/2/")
        self.assertContains(response, "I have lost my cat! Please help")
        self.assertNotContains(response, "Another short comment")

    def test_delete_comment_unauthorised(self):
        self.client.login(username="anna", password="password")
        response = self.client.get("/post/2/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I have lost my cat! Please help")
        self.assertContains(response, "Another short comment")
        response = self.client.post(
            "/post/2/comment/4/delete/",
            {"_save": "SAVE"},
        )
        self.assertEqual(response.status_code, 403)
        response = self.client.get("/post/2/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I have lost my cat! Please help")
        self.assertContains(response, "Another short comment")

    def test_update_comment_unauthorised(self):
        self.client.login(username="marie", password="password")
        response = self.client.get("/post/2/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I have lost my cat! Please help")
        self.assertNotContains(response, "This comment has been edited")
        response = self.client.post(
            "/post/2/comment/2/update/",
            {"body": "This comment has been edited", "_save": "SAVE"},
        )
        self.assertEqual(response.status_code, 403)
        response = self.client.get("/post/2/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I have lost my cat! Please help")
        self.assertNotContains(response, "This comment has been edited")

    def test_add_comment_anonimous_user(self):
        response = self.client.get("/post/1/comment/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/post/1/comment/")

    def test_update_comment_anonimous_user(self):
        response = self.client.get("/post/2/comment/2/update/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/post/2/comment/2/update/")

    def test_delete_comment_anonimous_user(self):
        response = self.client.get("/post/2/comment/4/delete/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/user/login/?next=/post/2/comment/4/delete/")
