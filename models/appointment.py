from app import db
from datetime import datetime

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patientID = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctorID = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    AppointmentDateTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    patient = db.relationship('Patient', backref='appointments')
    doctor = db.relationship('Doctor', backref='appointments')