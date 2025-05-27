from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from routes.db_config import get_db_connection

doctors = Blueprint("doctors", __name__)

@doctors.route("/doctors")
def doctor_list():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM doctors")
    doctor_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("doctors.html", doctors=doctor_data)

@doctors.route("/add_doctor", methods=["GET", "POST"])
def add_doctor():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        name = request.form["name"]
        specialization = request.form["specialization"]
        contact = request.form["contact"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO doctors (name, specialization, contact)
            VALUES (%s, %s, %s)
        """, (name, specialization, contact))
        conn.commit()
        cursor.close()
        conn.close()

        flash("Doctor added successfully!")
        return redirect(url_for("doctors.doctor_list"))

    return render_template("add_doctor.html")
