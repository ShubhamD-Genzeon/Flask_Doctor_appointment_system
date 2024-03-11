from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    doctor_quali = db.Column(db.String(255), nullable=False)
    specialization = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
