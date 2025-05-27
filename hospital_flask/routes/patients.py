from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from routes.db_config import get_db_connection

patients = Blueprint('patients', __name__, url_prefix='/patients')

@patients.route("/list")
def patient_list():
    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Use your actual primary key column name instead of 'id'
    cursor.execute("SELECT * FROM patients")  # Changed 'id' to 'patient_id'
    
    patient_data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('patients.html', patients=patient_data)

@patients.route("/add", methods=["GET", "POST"])
def add_patient():
    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        contact = request.form.get("contact")
        address = request.form.get("address")

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO patients (name, age, gender, contact, address)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, age, gender, contact, address))
            conn.commit()
            flash("Patient added successfully!", "success")
        except Exception as e:
            conn.rollback()
            flash(f"Error adding patient: {str(e)}", "danger")
        finally:
            cursor.close()
            conn.close()
        
        return redirect(url_for("patients.patient_list"))  # Redirect to patient list

    return render_template("add_patient.html")

@patients.route('/view/<int:id>')
def view_patient(id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patients WHERE id = %s", (id,))
    patient = cursor.fetchone()
    cursor.close()
    conn.close()

    if not patient:
        flash("Patient not found", "danger")
        return redirect(url_for("patients.patient_list"))

    return render_template("view_patient.html", patient=patient)

@patients.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        # Handle form submission
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        contact = request.form.get("contact")
        address = request.form.get("address")

        try:
            cursor.execute("""
                UPDATE patients 
                SET name=%s, age=%s, gender=%s, contact=%s, address=%s
                WHERE id=%s
            """, (name, age, gender, contact, address, id))
            conn.commit()
            flash("Patient updated successfully!", "success")
        except Exception as e:
            conn.rollback()
            flash(f"Error updating patient: {str(e)}", "danger")
        finally:
            cursor.close()
            conn.close()
        
        return redirect(url_for("patients.view_patient", id=id))

    # GET request - show edit form
    try:
        cursor.execute("SELECT * FROM patients WHERE id = %s", (id,))
        patient = cursor.fetchone()
        
        if not patient:
            flash("Patient not found", "danger")
            return redirect(url_for("patients.patient_list"))
            
        return render_template("edit_patient.html", patient=patient)
    finally:
        cursor.close()
        conn.close()

@patients.route('/delete/<int:id>')
def delete_patient(id):
    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM patients WHERE id = %s", (id,))
        conn.commit()
        flash("Patient deleted successfully", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error deleting patient: {str(e)}", "danger")
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for("patients.patient_list"))