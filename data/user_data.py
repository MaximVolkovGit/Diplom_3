from faker import Faker

class Person:
    """Метод генерации данных для регистрации"""

    @staticmethod
    def create_data_correct_user():
        faker = Faker('ru_RU')
        data = {
            "email": faker.email(),
            "password": faker.password(length=10),
            "name": faker.first_name()
        }
        return data