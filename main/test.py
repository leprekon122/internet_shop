from django.test import TestCase, Client
from django.urls import reverse
from .models import *
from .forms import *
from rest_framework.test import APITestCase

"""Test (get request) on templates """


class TestGet(TestCase):

    def setUp(self):
        self.client = Client()

    def test_main_page(self):
        response = self.client.get(reverse('main'))

        self.assertEqual(response.status_code, 200)

    def test_main_laptop_page(self):
        response = self.client.get(reverse('note_main'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/nothebook.html')

    def test_main_videcards_page(self):
        response = self.client.get(reverse('videocards'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/videocards.html')

    def test_main_display_page(self):
        response = self.client.get(reverse('displays'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/displays.html')

    def test_main_memory_page(self):
        response = self.client.get(reverse('memory'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/memory.html')


"""Test post registration page"""


class TestPost(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('registration')
        self.url_note = reverse('note_main')

    def test_registration(self):
        response = self.client.post(self.url, {
            'username': 'test',
            'password1': '12011993gCp',
            'password2': '12011993gCp',
            'email': '1234@gmail.com'
        })
        self.assertEqual(response.status_code, 302)


"""Test_all_models"""


class TestModels(TestCase):

    def test_registration(self):
        User.objects.create(username='nick', password='123', email='123@gmail.com')
        user = User.objects.filter(username='nick').values()[0]

        self.assertTrue(user['username'] == 'nick')

    def test_likeListModel(self):
        user = User.objects.create(username='nick', password='123', email='123@gmail.com')

        LikeListModel.objects.create(user_name=user, product_title='test', product_pic='test', product_price=123,
                                     product_status='Є в наявності')

        model = LikeListModel.objects.filter(id=1).values()[0]

        self.assertTrue(model['product_title'] == 'test')

    def test_porodactCartModel(self):
        user = User.objects.create(username='nick', password='123', email='123@gmail.com')

        ProductCart.objects.create(user_name=user, product_title='test', product_pic='test',
                                   product_price=123, product_status='Є в наявності')

        model = ProductCart.objects.filter(id=1).values()[0]

        self.assertTrue(model['product_title'] == 'test')

    def test_NotebookList(self):
        NotebooksList.objects.create(brand='Apple', title='test_apple', video_link='test',
                                     pic='Shop/media/monitors_pic/amd.jpeg', pic_link='test',
                                     description='test',
                                     price=123, in_out='Є в наявності')

        model = NotebooksList.objects.filter(id=1).values()[0]
        self.assertTrue(model['title'] == 'test_apple')

    def test_VideocardsList(self):
        Videocards.objects.create(brand='Asus', title='test_asus', video_link='test',
                                  pic='Shop/media/monitors_pic/amd.jpeg', pic_link='test',
                                  description='test',
                                  price=123, in_out='Є в наявності')

        model = Videocards.objects.filter(id=1).values()[0]
        self.assertTrue(model['title'] == 'test_asus')

    def test_MonitorsList(self):
        Monitors_list.objects.create(brand='Asus', title='test_asus', video_link='test',
                                     pic='Shop/media/monitors_pic/amd.jpeg', pic_link='test',
                                     description='test',
                                     price=123, in_out='Є в наявності')

        model = Monitors_list.objects.filter(id=1).values()[0]
        self.assertTrue(model['title'] == 'test_asus')

    def test_MemoryList(self):
        Memory_list.objects.create(brand='Kingston', title='test_Kingston', video_link='test',
                                   pic='Shop/media/monitors_pic/amd.jpeg', pic_link='test',
                                   description='test',
                                   price=123, in_out='Є в наявності')

        model = Memory_list.objects.filter(id=1).values()[0]
        self.assertTrue(model['title'] == 'test_Kingston')


"""Test registration form"""


class TestForm(TestCase):

    def test_form(self):
        form = UserCreationForm(data={
            'username': 'nick_1',
            'password1': '12011993gCp',
            'password2': '12011993gCp',
            'email': '123@gmail.com'
        })

        self.assertTrue(form.is_valid())


"""Test APi"""


class TestApi(APITestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('note_api')

    def test_api(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
