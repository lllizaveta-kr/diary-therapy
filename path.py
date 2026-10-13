import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def resource_path(*parts):
    """Возвращает абсолютный путь к файлу внутри проекта."""
    return os.path.join(BASE_DIR, *parts)

def images_path(filename):
    return resource_path("images", filename)