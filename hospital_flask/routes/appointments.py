from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from routes.db_config import get_db_connection

appointments = Blueprint('appointments', __name__, url_prefix='/appointments')
@appointments.route("/add", methods=["GET", "POST"])
def add_appointment():
    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect(url_for("auth.login"))

    # Initialize variables with default values
    patients = []
    doctors = []
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get patients and doctors
        cursor.execute("SELECT patient_id, name FROM patients WHERE is_active = 1 ORDER BY name")
        patients = cursor.fetchall()
        
        cursor.execute("SELECT doctor_id, name, specialization FROM doctors WHERE is_active = 1 ORDER BY name")
        doctors = cursor.fetchall()

        if request.method == "POST":
            # Validate form data
            required_fields = ['patient_id', 'doctor_id', 'date', 'time']
            if not all(field in request.form for field in required_fields):
                flash("Please fill all required fields", "danger")
                return render_template("add_appointment.html",
                                    patients=patients,
                                    doctors=doctors)

            # Process form submission
            patient_id = request.form["patient_id"]
            doctor_id = request.form["doctor_id"]
            appointment_datetime = f"{request.form['date']} {request.form['time']}:00"
            reason = request.form.get("reason", "Not specified")

            # Check for conflicts
            cursor.execute("""
                SELECT appointment_id FROM appointments 
                WHERE doctor_id = %s AND appointment_date = %s
                AND status != 'cancelled'
            """, (doctor_id, appointment_datetime))
            
            if cursor.fetchone():
                flash("Doctor already has an appointment at this time", "warning")
                return render_template("add_appointment.html",
                                    patients=patients,
                                    doctors=doctors)

            # Insert new appointment
            cursor.execute("""
                INSERT INTO appointments 
                (patient_id, doctor_id, appointment_date, reason, status)
                VALUES (%s, %s, %s, %s, 'scheduled')
            """, (patient_id, doctor_id, appointment_datetime, reason))
            
            conn.commit()
            flash("Appointment booked successfully!", "success")
            return redirect(url_for("appointments.list"))

    except Exception as e:
        conn.rollback()
        flash(f"Database error: {str(e)}", "danger")
        # Log the error for debugging
        print(f"Appointment booking error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

    # Render template with current data (works for both GET and failed POST)
    return render_template("add_appointment.html",
                         patients=patients,
                         doctors=doctors,
                         current_date=datetime.now().strftime("%Y-%m-%d"))

@appointments.route("/list")
def list():
    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT a.appointment_id, a.appointment_date, a.status, a.reason,
                   p.name as patient_name, p.patient_id,
                   d.name as doctor_name, d.specialization
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
            ORDER BY a.appointment_date DESC
        """)
        appointments = cursor.fetchall()
        
        return render_template("appointment_list.html",
                             appointments=appointments)
    except Exception as e:
        flash(f"Error retrieving appointments: {str(e)}", "danger")
        return render_template("appointment_list.html",
                             appointments=[])
    finally:
        cursor.close()
        conn.close()

@appointments.route("/cancel/<int:appointment_id>")
def cancel(appointment_id):
    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE appointments 
            SET status = 'cancelled' 
            WHERE appointment_id = %s
        """, (appointment_id,))
        conn.commit()
        flash("Appointment cancelled successfully", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error cancelling appointment: {str(e)}", "danger")
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for("appointments.list"))