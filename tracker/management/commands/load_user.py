from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


TEST_USERNAME = "user"
TEST_PASSWORD = "12345"


class Command(BaseCommand):
    help = "Создает тестового пользователя"

    def handle(self, *args, **options):
        test_user = User.objects.filter(username=TEST_USERNAME)
        if test_user:
            test_user.delete()
            self.stdout.write("Удаление старого пользователя")

        new_user = User.objects.create(
            username="user",
            email="1@ya.ru",
        )
        new_user.set_password(TEST_PASSWORD)
        new_user.save()
        self.stdout.write("Пользователь создан")
