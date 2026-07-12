import os

# ეს ფაილი ინახავს ყველა კონფიგურაციას ერთ ადგილას რომ არ მომიწიოს
# მაგიური სტრიქონების ძებნა app.py-ში ყოველ ჯერზე

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")

if not os.path.exists(INSTANCE_DIR):
    os.makedirs(INSTANCE_DIR)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(INSTANCE_DIR, "platform.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # ეს გამორთული უნდა იყოს, warning-ებს იძლევა

    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")
