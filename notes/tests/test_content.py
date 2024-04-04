from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestNoteContent(TestCase):
    """Набор тестов для проверки контента создания заметок."""

    @classmethod
    def setUpTestData(cls):
        """Подготовка данных для тестов."""
        cls.reader = User.objects.create(username='reader')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.reader)
        cls.author = User.objects.create(username='author')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)
        cls.note_author = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author)
        cls.note_reader = Note.objects.create(
            title='Заголовок Читателя',
            text='Текст Читателя',
            author=cls.reader
        )
        cls.url = reverse('notes:list')
        cls.add_url = reverse('notes:add', None)

    def test_note_is_not_in_object_list_for_another_user(self):
        """
        Проверка, что в список заметок одного пользователя не
        попадают заметки другого пользователя.
        """
        user = self.reader
        self.client.force_login(user)
        response = self.client.get(self.url)
        object_list = response.context['object_list']
        self.assertNotIn(self.note_author, object_list)

    def test_single_note_in_object_list(self):
        """
        Проверка, что отдельная заметка передается
        на страницу со списком заметок
        в списке object_list в словаре context.
        """
        user = self.reader
        self.client.force_login(user)
        response = self.client.get(self.url)
        object_list = response.context['object_list']
        self.assertIn(self.note_reader, object_list)

    def test_edit_has_form(self):
        user = self.author
        self.client.force_login(user)
        note_from_author = Note.objects.filter(author=self.author).first()
        url = reverse('notes:edit', args=(note_from_author.slug,))
        response = self.client.get(url)
        self.assertIn('form', response.context)

    def test_add_has_form(self):
        user = self.author
        self.client.force_login(user)
        response = self.client.get(self.add_url)
        self.assertIn('form', response.context)
