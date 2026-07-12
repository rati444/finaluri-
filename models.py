from datetime import datetime, timezone

from werkzeug.security import generate_password_hash, check_password_hash

from ext import db


def now_utc():
    # UTC-ს ვიყენებ რომ არ დამებნეს დროის სარტყლებში სერვერსა და ჩემს კომპიუტერს შორის
    return datetime.now(timezone.utc)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="student")  # student / teacher / admin
    created_at = db.Column(db.DateTime, default=now_utc)

    resources = db.relationship("Resource", backref="uploader", lazy=True)

    def set_password(self, raw_password):
        # პაროლს არასდროს ვინახავ plain text-ად, ჰეშირებას werkzeug აკეთებს
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat(),
        }


class Resource(db.Model):
    __tablename__ = "resources"

    # ფაილების ატვირთვის გარეშე ვინახავ მხოლოდ ინფორმაციას მასალაზე
    # (სათაური, საგანი და ვინ დაამატა) - ნამდვილი ფაილი აქ აღარ ინახება
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(80), nullable=False, index=True)
    semester = db.Column(db.String(40), nullable=False)
    resource_type = db.Column(db.String(40), nullable=False, default="კონსპექტი")

    uploader_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=now_utc)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "subject": self.subject,
            "semester": self.semester,
            "resource_type": self.resource_type,
            "uploader": self.uploader.full_name if self.uploader else "უცნობი",
            "created_at": self.created_at.isoformat(),
        }
