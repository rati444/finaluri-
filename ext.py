"""
ყველა გაფართოება (extension) ერთ ადგილას, რომ არ მქონდეს
წრიული იმპორტების პრობლემა app.py, models.py და routes.py-ს შორის.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
