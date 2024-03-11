from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///doctor_appoint_system.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key' 
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment

@app.route('/')
def hello_world():
    # new_doctor= Doctor(name="Ayush Upadhyay",doctor_quali="M.D, MBBS" ,specialization="Gynecologist", password_hash="vk123" )
    # db.session.add(new_doctor)
    # db.session.commit()
    return render_template('index.html')

@app.route('/register')
def register_patient_form():
    return render_template('register.html')

@app.route('/register_patient', methods=['POST'])
def register_patient():
    if request.method == 'POST':
        username = request.form['username']
        userEmail = request.form['userEmail']
        phoneNumber = request.form['phoneNumber']
        password = request.form['password']
        new_patient = Patient(username=username, userEmail=userEmail, phoneNumber=phoneNumber)
        print(new_patient)
        new_patient.set_password(password)
        db.session.add(new_patient)
        db.session.commit()
        flash('Patient registered successfully!', 'success')
        return render_template('index.html', flash_message='Patient registered successfully! Please log in.')
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        patient = Patient.query.filter_by(username=username).first()
        if patient and patient.check_password(password):
            flash('Login successful!', 'success')
            session['patient_id'] = patient.id  # Store patient ID in session
            return redirect(url_for('doctors_list'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    return render_template('index.html')

@app.route('/doctors')
def doctors_list():
    if 'patient_id' in session:
        patient_id = session['patient_id']  # Retrieve patient ID from session
        doctors = Doctor.query.all()
        return render_template('book_appointment.html', doctors=doctors, patient_id=patient_id)
    else:
        flash('Please login first.', 'danger')
        return redirect(url_for('login'))

@app.route('/booking')
def booking():
    doctor_id = request.args.get('doctor_id')
    patient_id = request.args.get('patient_id')
    return render_template('booking.html', doctor_id=doctor_id, patient_id=patient_id)

@app.route('/confirm_appointment', methods=['POST'])
def confirm_appointment():
    doctor_id = request.form['doctor_id']
    patient_id = request.form['patient_id']
    appointment_date_str = request.form['appointment_date']
    appointment_time_str = request.form['appointment_time']
    
    # Combine date and time strings into a single datetime object
    appointment_datetime_str = f"{appointment_date_str} {appointment_time_str}"
    appointment_datetime = datetime.strptime(appointment_datetime_str, '%Y-%m-%d %H:%M')

    # Creating the appointment in the Appointment table
    new_appointment = Appointment(
        doctorID=doctor_id,
        patientID=patient_id,
        AppointmentDateTime=appointment_datetime
    )
    db.session.add(new_appointment)
    db.session.commit()
    flash('Appointment confirmed successfully!', 'success')
    return redirect(url_for('doctors_list'))


@app.route('/your-appointments')
def your_appointments():
    # Get the patient ID from the session
    patient_id = session.get('patient_id')

    if patient_id:
        # Query the appointments associated with the patient ID and join with the Doctor table
        appointments = db.session.query(Appointment, Doctor).filter(
            Appointment.patientID == patient_id,
            Appointment.doctorID == Doctor.id
        ).all()

        return render_template('my_appointments.html', appointments=appointments)
    else:
        # Redirect to login or handle the case when the patient ID is not in the session
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    # Remove patient ID from the session
    session.pop('patient_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('hello_world'))
    
if __name__ == "__main__":
    app.run(debug=True)
