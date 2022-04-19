from django.test import TestCase


class ProfileTestCase(TestCase):
    fixtures = [
        "user_test.json",
        "profile_test.json",
        "category_test.json",
        "post_test.json",
        "comment_test.json",
    ]

    def test_register(self):
        response = self.client.get("/user/register/")
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            "/user/register/",
            {
                "username": "new_user",
                "password1": "new_password",
                "password2": "new_password",
                "email": "test@email.com",
                "postcode": "8305",
                "city": "Berlin",
                "_save": "SAVE",
            },
        )
        self.assertRedirects(response, "/user/login/")
        response = self.client.get("/")
        self.assertRedirects(response, "/user/login/?next=/")
        self.client.login(username="new_user", password="new_password")
        response = self.client.get("/")
        self.assertContains(response, "Has anybody seen my cow")

    def test_not_register_with_false_postcode(self):
        response = self.client.get("/user/register/")
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            "/user/register/",
            {
                "username": "new_user",
                "password1": "new_password",
                "password2": "new_password",
                "email": "test@email.com",
                "postcode": "8303",
                "city": "Berlin",
                "_save": "SAVE",
            },
        )
        self.assertContains(response, "Only people from island Samsø can register")

    def test_create_profile_with_registration(self):
        response = self.client.get("/user/register/")
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            "/user/register/",
            {
                "username": "new_user",
                "password1": "new_password",
                "password2": "new_password",
                "email": "test@email.com",
                "postcode": "8305",
                "city": "Berlin",
                "_save": "SAVE",
            },
        )
        self.assertRedirects(response, "/user/login/")
        response = self.client.get("/user/profile/")
        self.assertRedirects(response, "/user/login/?next=/user/profile/")
        self.client.login(username="new_user", password="new_password")
        response = self.client.get("/user/profile/")
        self.assertContains(response, "new_user")

    def test_delete_profile(self):
        self.client.login(username="anna", password="password")
        response = self.client.get("/user/profile/")
        self.assertContains(response, "anna")
        response = self.client.post("/user/delete/")
        response = self.client.get("/user/profile/")
        self.assertRedirects(response, "/user/login/?next=/user/profile/")
        self.client.login(username="anna", password="password")
        response = self.client.get("/user/profile/")
        self.assertRedirects(response, "/user/login/?next=/user/profile/")
