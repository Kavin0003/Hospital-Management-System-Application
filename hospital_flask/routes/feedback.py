from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from routes.db_config import get_db_connection

feedback = Blueprint("feedback", __name__)

@feedback.route("/feedback")
def feedback_list():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT f.id, p.name AS patient_name, d.name AS doctor_name, f.rating, f.comments
        FROM feedback f
        JOIN patients p ON f.patient_id = p.id
        JOIN doctors d ON f.doctor_id = d.id
    """)
    feedbacks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("feedback.html", feedbacks=feedbacks)

@feedback.route("/add_feedback", methods=["GET", "POST"])
def add_feedback():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        patient_id = request.form["patient_id"]
        doctor_id = request.form["doctor_id"]
        rating = request.form["rating"]
        comments = request.form["comments"]

        cursor.execute("""
            INSERT INTO feedback (patient_id, doctor_id, rating, comments)
            VALUES (%s, %s, %s, %s)
        """, (patient_id, doctor_id, rating, comments))
        conn.commit()
        flash("Feedback submitted successfully!")
        return redirect(url_for("feedback.feedback_list"))

    cursor.execute("SELECT id, name FROM patients")
    patients = cursor.fetchall()
    cursor.execute("SELECT id, name FROM doctors")
    doctors = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("add_feedback.html", patients=patients, doctors=doctors)