from flask import Flask, redirect, url_for
from routes.auth import auth_bp
from routes.dashboard import dashboard
from routes.patients import patients
from routes.doctors import doctors
from routes.appointments import appointments
from routes.billing import billing
from routes.feedback import feedback
from routes.inventory import inventory
from routes.medical_records import medical_records
from routes.staff import staff

app = Flask(__name__)
app.secret_key = "ad826e665c7e73fc236ee542ee08c0bee72bc7786d7c765bfecd3005169a504d"

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dashboard, url_prefix='/dashboard')  
app.register_blueprint(patients, url_prefix='/patients')    
app.register_blueprint(doctors, url_prefix='/doctors')
app.register_blueprint(appointments, url_prefix='/appointments')
app.register_blueprint(billing, url_prefix='/billing')
app.register_blueprint(feedback, url_prefix='/feedback')
app.register_blueprint(inventory, url_prefix='/inventory')
app.register_blueprint(medical_records, url_prefix='/medical')
app.register_blueprint(staff, url_prefix='/staff')

@app.route('/')
def home():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
