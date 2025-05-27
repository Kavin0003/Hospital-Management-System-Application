from flask import Blueprint, render_template, session, redirect, url_for

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/dashboard")
def home():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    return render_template("dashboard.html", username=session.get("username"))

@dashboard.route("/patients/list")
def patient_list():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    return render_template("patients.html")

@dashboard.route("/doctors")
def doctors():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    return render_template("doctors.html")



@dashboard.route("/appointments")
def appointments():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    return render_template("appointments.html")

@dashboard.route("/billing")
def billing():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    return render_template("billing.html")

@dashboard.route("/staff")
def staff():
    if "username" not in session:
        return redirect(url_for("auth.login"))
    return render_template("staff.html", username=session.get("username"))