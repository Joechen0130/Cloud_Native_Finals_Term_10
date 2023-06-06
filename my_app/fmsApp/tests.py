from django.test import TestCase, RequestFactory
from django.urls import reverse, resolve
from fmsApp.views import PollHistoryView, registerUser, home, public
# Create your tests here.
# 初始劃一個author 提供後續使用
from fmsApp.models import Post
from fmsApp.forms import UserRegistration
from django.test import SimpleTestCase
from django.utils import timezone
from django.contrib.auth.models import User
from .views import *

class view_test(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.test_user = User.objects.create_user(username='test2', password="test2222")
        self.test_thing = Post.objects.create(user=self.test_user,
                                              title="test_1234")

        self.assertTrue((self.test_user is not None) and self.test_user.is_authenticated)
    def test_form_manage_post(self):
        test_thing = Post.objects.get(title="test_1234")
        self.client.login(username='test2', password='test2222')
        response = self.client.post('/accounts/home/')
        print("==============================")
        print(response)

# model
class Postmodel_test(TestCase):
    def test_create_user(self):
        test_user = User.objects.create_user(username="test1",
                                             email='e1@app.com')
        test_user.save()
        post = Post(user = test_user)
        post.save()
        self.assertEqual(str(post), "test1-")
    
    def test_create_user_title(self):
        test_user = User.objects.create_user(username="test1")
        test_user.save()
        post_title = Post(user = test_user, title="test1234")
        post_title.save()
        self.assertEqual(str(post_title), "test1-test1234")

    def test_create_user_filepath(self):
        test_user = User.objects.create_user(username="test1")
        test_user.save()
        post_title_file = Post(user = test_user, file_path='uploads3')
        post_title_file.save()
        self.assertEqual(str(post_title_file), "test1-")
    
        
# # 以下為寫要寫測試的功能
# url
class TestBlogUrls(SimpleTestCase):
    
    def test_url_history(self):
        url = reverse('history')
        self.assertEquals(resolve(url).func.view_class, PollHistoryView)
    
    def test_url_public(self):
        url1 = reverse('register-user')
        self.assertEquals(resolve(url1).func, registerUser)

    def test_url_home(self):
        url2 = reverse('home-page')
        self.assertEquals(resolve(url2).func, home)

    def test_public(self):
        url3 = reverse('public')
        self.assertEquals(resolve(url3).func, public)






        
