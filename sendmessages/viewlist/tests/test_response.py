from django.test import TestCase
from ..models import TaskList


class ResponseTest(TestCase):
    def test_main_page(self):
        """
        Главная страница использует шаблон viewlist.html
        """
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'viewlist/viewlist.html')

    def test_view_free(self):
        """
        Отображение на странице "Список рассылки пуст" когда таблица "TaskList" пустая
        :return:
        """
        response = self.client.get('')
        self.assertContains(response, "Список рассылки пуст", status_code=response.status_code)

    def test_view_record_name(self):
        """
        Отображение на странице поля "name" таблицы "TaskList"
        :return:
        """
        TaskList.objects.create(name="text_test_name")
        response = self.client.get('')
        self.assertContains(response, "text_test_name", status_code=response.status_code)

