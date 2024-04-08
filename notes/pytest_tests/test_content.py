from django.urls import reverse

# В тесте используем фикстуру заметки
# и фикстуру клиента с автором заметки.
def test_note_in_list_for_author(note, author_client):
    url = reverse('notes:list')
    # Запрашиваем страницу со списком заметок:
    response = author_client.get(url)
    # Получаем список объектов из контекста:
    object_list = response.context['object_list']
    # Проверяем, что заметка находится в этом списке:
    assert note in object_list


# В этом тесте тоже используем фикстуру заметки,
# но в качестве клиента используем not_author_client;
# в этом клиенте авторизован не автор заметки, 
# так что заметка не должна быть ему видна.
def test_note_not_in_list_for_another_user(note, not_author_client):
    url = reverse('notes:list')
    response = not_author_client.get(url)
    object_list = response.context['object_list']
    # Проверяем, что заметки нет в контексте страницы:
    assert note not in object_list