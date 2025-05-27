from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from routes.db_config import get_db_connection

staff = Blueprint("staff", __name__)

@staff.route("/staff")
def staff_list():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM staff")
    staff_members = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("staff.html", staff=staff_members)

@staff.route("/add_staff", methods=["GET", "POST"])
def add_staff():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        name = request.form["name"]
        role = request.form["role"]
        contact = request.form["contact"]
        email = request.form["email"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO staff (name, role, contact, email)
            VALUES (%s, %s, %s, %s)
        """, (name, role, contact, email))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Staff member added successfully!")
        return redirect(url_for("staff.staff_list"))

    return render_template("add_staff.html")
