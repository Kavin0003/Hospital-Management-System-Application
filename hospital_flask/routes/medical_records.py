from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from routes.db_config import get_db_connection

medical_records = Blueprint("medical_records", __name__)

@medical_records.route("/medical_records")
def record_list():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT mr.id, p.name AS patient_name, mr.diagnosis, mr.treatment, mr.prescription
        FROM medical_records mr
        JOIN patients p ON mr.patient_id = p.id
    """)
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("medical_records.html", records=records)

@medical_records.route("/add_medical_record", methods=["GET", "POST"])
def add_record():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        patient_id = request.form["patient_id"]
        diagnosis = request.form["diagnosis"]
        treatment = request.form["treatment"]
        prescription = request.form["prescription"]

        cursor.execute("""
            INSERT INTO medical_records (patient_id, diagnosis, treatment, prescription)
            VALUES (%s, %s, %s, %s)
        """, (patient_id, diagnosis, treatment, prescription))
        conn.commit()
        flash("Medical record added successfully!")
        return redirect(url_for("medical_records.record_list"))

    cursor.execute("SELECT id, name FROM patients")
    patients = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("add_medical_record.html", patients=patients)
