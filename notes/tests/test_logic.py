from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from notes.models import Note

User = get_user_model()


class TestCommentCreation(TestCase):
    # Текст заметки понадобится в нескольких местах кода,
    # поэтому запишем его в атрибуты класса.
    NOTE_TEXT = 'Текст заметки'

    @classmethod
    def setUpTestData(cls):
        # Создаём пользователя и клиент, логинимся в клиенте.
        cls.user = User.objects.create(username='Марти')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        # URL для страницы создания заметки.
        cls.url = reverse('notes:add')
        # Данные для POST-запроса при создании заметки.
        cls.form_data = {'title': 'Заголовок', 'text': cls.NOTE_TEXT}

    def test_anonymous_user_cant_create_note(self):
        # Совершаем запрос от анонимного клиента, в POST-запросе отправляем
        # предварительно подготовленные данные формы с текстом заметки.
        self.client.post(self.url, data=self.form_data)
        # Считаем количество заметок.
        notes_count = Note.objects.count()
        # Ожидаем, что заметок в базе нет - сравниваем с нулём.
        self.assertEqual(notes_count, 0)

    def test_user_can_create_note(self):
        # Совершаем запрос через авторизованный клиент.
        response = self.auth_client.post(self.url, data=self.form_data)
        # Проверяем, что URL перенаправления корректен
        self.assertEqual(response.url, reverse('notes:success'))
        # Проверяем, что заметка была создана
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        # Получаем созданную заметку из базы данных
        note = Note.objects.get()
        # Проверяем, что атрибуты заметки соответствуют ожидаемым значениям
        self.assertEqual(note.text, self.NOTE_TEXT)
        self.assertEqual(note.author, self.user)