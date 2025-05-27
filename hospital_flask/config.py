from flask import Flask
from flask_session import Session

# Import blueprints from routes
from routes.auth import auth
from routes.patients import patient
from routes.doctors import doctor
from routes.appointments import appointment
from routes.medical_records import medical
from routes.billing import billing
from routes.feedback import feedback
from routes.staff import staff
from routes.inventory import inventory
from routes.dashboard import dashboard

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(patient)
app.register_blueprint(doctor)
app.register_blueprint(appointment)
app.register_blueprint(medical)
app.register_blueprint(billing)
app.register_blueprint(feedback)
app.register_blueprint(staff)
app.register_blueprint(inventory)
app.register_blueprint(dashboard)

if __name__ == '__main__':
    app.run(debug=True)
