"""
დამხმარე სკრიპტი მონაცემთა ბაზის მიგრაციისთვის Flask-Migrate-ის გამოყენებით.

ტერმინალში, პირველად საჭირო ბრძანებები:
    flask --app run db init
    flask --app run db migrate -m "საწყისი მიგრაცია"
    flask --app run db upgrade

ან უბრალოდ გაუშვი ეს ფაილი, რომ პირდაპირ შეიქმნას ცხრილები
migration history-ის გარეშე (სწრაფი გზა დემოსთვის):
    python migrate.py
"""
from app import create_app
from ext import db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("ბაზის ცხრილები წარმატებით შეიქმნა (instance/platform.db).")
