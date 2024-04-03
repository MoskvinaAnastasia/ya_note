from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()



def test_note_is_not_in_object_list_for_another_user(self):
    # Создаем заметку для пользователя self.author
    note = Note.objects.create(title="Test Note", text="Test Text", author=self.author)

    # Авторизуемся как другой пользователь
    user = self.reader
    self.client.force_login(user)

    # Получаем URL для страницы списка заметок
    url = reverse('notes:list')

    # Отправляем GET-запрос к странице списка заметок
    response = self.client.get(url)

    # Получаем список объектов из контекста ответа
    object_list = response.context['object_list']

    # Проверяем, что заметка другого пользователя не присутствует в списке объектов
    self.assertNotIn(note, object_list)