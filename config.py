import os

# Для указания пути к файлу БД воспользумся путем до текущего модуля
# - Текущая папка
current_path = os.path.dirname(os.path.realpath(__file__))


class Config:
    DEBUG = True
    SECRET_KEY = "randomstringstepiktranslate"
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres:base@localhost:5432/stepik4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False