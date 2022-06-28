from django.test import TestCase
from main.models import *


class TestRegisterUser(TestCase):

    #def register_user(self):
    #    QuestionUsersMemory.objects.create(name_of_user='nick',
    #                                       name_of_stuff="Модуль пам'яті Crucial DDR4 16Gb (2x8) Ballistix Black 3200 Mhz (BL2K8G32C16U4B)",
    #                                       comment='test_of_test')

    def view_db(self):
        name = QuestionUsersMemory.objects.get(name='nick')
        print(name)
        self.assertEqual(name, 'nick')
