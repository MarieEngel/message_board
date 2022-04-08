import os
from time import sleep

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC  # noqa: N812
from post.models import Category

class SeleniumTestPost(StaticLiveServerTestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        if os.getenv("CI"):
            options.binary_location = "/usr/bin/google-chrome-stable"
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            self.driver = webdriver.Chrome(options=options)
        else:
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        self.user = User.objects.create_user(username="testuser1", password="password")
        self.category = Category.objects.create(name='Lost')

    def tearDown(self):
        self.user.delete()

    def test_add__post_form(self):
        """Tests excistence post form."""
        self.driver.get(f"{self.live_server_url}/user/login/")
        username_field = self.driver.find_element_by_name("username")
        username_field.send_keys("testuser1")
        password_field = self.driver.find_element_by_name("password")
        password_field.send_keys("password")
        login_button = self.driver.find_element_by_xpath("//button[@class='btn btn-submit-custom']")
        login_button.click()
        add_post_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "#navbarSupportedContent > ul > li:nth-child(2) > a",
                )
            )
        )
        add_post_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "id_title"))
        )
        title_fields = self.driver.find_elements_by_css_selector("#id_title")
        self.assertEqual(len(title_fields), 1)

    def test_add_post(self):
        """Tests adding a post."""
        self.driver.get(f"{self.live_server_url}/user/login/")
        username_field = self.driver.find_element_by_name("username")
        username_field.send_keys("testuser1")
        password_field = self.driver.find_element_by_name("password")
        password_field.send_keys("password")
        login_button = self.driver.find_element_by_xpath("//button[@class='btn btn-submit-custom']")
        login_button.click()
        add_post_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "#navbarSupportedContent > ul > li:nth-child(2) > a",
                )
            )
        )
        add_post_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "id_title"))
        )
        post_title = self.driver.find_element_by_css_selector("#id_title")
        post_title.send_keys('Missing cat')
        post_body = self.driver.find_element_by_name('body')
        post_body.send_keys('My cat did not come home.')

        select = Select(self.driver.find_element_by_name("category"))
        select.select_by_index(1)

        submit_button = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//button[@class='btn btn-submit-custom']",
                )
            )
        )
        # element = self.driver.find_element_by_xpath("//button[@class='btn btn-submit-custom']")
        # self.driver.execute_script("arguments[0].click();", submit_button)
        submit_button.click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "id_title"))
        )
        self.assertIsNotNone(self.driver.find_elements_by_class_name('//*[contains(text(), "My cat did not come home.")]'))
